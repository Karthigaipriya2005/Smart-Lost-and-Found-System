from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users app
    path('', include('users.urls', namespace='users')),

    # Persons app
    path('persons/', include('persons.urls', namespace='persons')),

    # in smart_lost_found/urls.py (if not present yet)
    path('items/', include('items.urls', namespace='items')),

    # smart_lost_found/urls.py
    path('adminpanel/', include('adminpanel.urls', namespace='adminpanel')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
