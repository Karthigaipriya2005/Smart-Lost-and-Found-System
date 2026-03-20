from django.urls import path
from . import views

app_name = "persons"

urlpatterns = [
    path('search_person/', views.search_person, name='search_person'),
]
