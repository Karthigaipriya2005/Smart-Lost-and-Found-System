from django.shortcuts import render
from django.conf import settings
from django.utils.text import get_valid_filename
import os
import cv2
from datetime import timedelta
from ai_module.person_reid import detect_and_match_person, extractor, yolo_model, PERSON_CLASS_ID

FRAME_SKIP = 3  # process every 3rd frame for speed

def search_person(request):
    context = {"results": [], "message": ""}

    if request.method == "POST":
        video_file = request.FILES.get("video")
        image_file = request.FILES.get("image")

        if not video_file or not image_file:
            context["message"] = "⚠️ Please upload both CCTV video and person image."
            return render(request, "persons/search_person.html", context)

        # --- Save uploaded files ---
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        video_path = os.path.join(upload_dir, get_valid_filename(video_file.name))
        with open(video_path, "wb+") as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        image_path = os.path.join(upload_dir, get_valid_filename(image_file.name))
        with open(image_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # --- Preprocess query image ---
        query_img = cv2.imread(image_path)
        query_results = yolo_model(query_img, classes=[PERSON_CLASS_ID], conf=0.25)

        if len(query_results[0].boxes.xyxy) == 0:
            query_crop = query_img  # fallback to full image
        else:
            x1, y1, x2, y2 = map(int, query_results[0].boxes.xyxy[0].cpu().numpy())
            query_crop = query_img[y1:y2, x1:x2]

        query_crop = cv2.resize(query_crop, (128, 256))
        query_feature = extractor([query_crop])[0]

        # --- Open Video ---
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            context["message"] = "❌ Could not open video file."
            return render(request, "persons/search_person.html", context)

        results = []
        last_saved_timestamp = None
        detected_features = {}
        output_dir = os.path.join(settings.MEDIA_ROOT, "matches")
        os.makedirs(output_dir, exist_ok=True)

        frame_num = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_num += 1
            if frame_num % FRAME_SKIP != 0:
                continue

            timestamp_sec = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
            timestamp_str = str(timedelta(seconds=timestamp_sec))

            if timestamp_str not in detected_features:
                detected_features[timestamp_str] = []

            match_found, annotated_frame, updated_features, max_sim = detect_and_match_person(
                frame, query_feature, detected_features[timestamp_str], threshold=0.5
            )
            detected_features[timestamp_str] = updated_features

            # Save matched frame
            if match_found and last_saved_timestamp != timestamp_str:
                last_saved_timestamp = timestamp_str
                result_filename = f"match_{timestamp_sec}s.jpg"
                result_path = os.path.join(output_dir, result_filename)
                annotated_frame = cv2.resize(annotated_frame, (640, 360))
                cv2.imwrite(result_path, annotated_frame)

                # Instead of os.path.join("matches", result_filename)
                results.append({
                    "img": os.path.join(settings.MEDIA_URL, "matches", result_filename),
                    "time": timestamp_str
                    })


        cap.release()
        context["results"] = results
        context["message"] = f"{len(results)} match(es) found." if results else "No matching person found."

    return render(request, "persons/search_person.html", context)
