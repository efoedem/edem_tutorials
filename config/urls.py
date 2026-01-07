from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),

    # 2. Home page (Redirects to course list)
    path('', lambda request: redirect('course_list', permanent=False)),

    # 3. Your App URLs
    path('courses/', include('apps.courses.urls')),
    path('enrollments/', include('apps.enrollments.urls')),

    # 4. Authentication URLs (ADD THIS LINE)
    # This handles the login redirect that was giving you the 404
    path('accounts/', include('django.contrib.auth.urls')),
]