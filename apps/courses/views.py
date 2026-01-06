from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Course
from django.shortcuts import render, get_object_or_404 # Add get_object_or_404
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})



# ... keep your course_list view here ...

def course_detail(request, pk):
    # This looks for the course by ID; if it doesn't exist, it shows a 404 page
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})