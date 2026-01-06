from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # 1. Fix the admin typo (changed py_admin to urls)
    path('admin/', admin.site.urls),

    # 2. Fix the home page (redirects / to /courses/)
    path('', lambda request: redirect('course_list', permanent=False)),

    # 3. Your App URLs
    path('courses/', include('apps.courses.urls')),
    path('enrollments/', include('apps.enrollments.urls')),
]