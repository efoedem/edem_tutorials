from django.urls import path
from .views import course_list, course_detail # Import the new view

urlpatterns = [
    path('', course_list, name='course_list'),
    # This captures the ID (pk) from the URL, like /courses/1/
    path('<int:pk>/', course_detail, name='course_detail'),
]