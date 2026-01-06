import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Enrollment
from apps.courses.models import Course
from .forms import EnrollmentDetailsForm

@login_required
def initiate_enrollment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = EnrollmentDetailsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('payment_instruction', course_id=course.id)
    else:
        form = EnrollmentDetailsForm(instance=request.user)

    return render(request, 'enrollments/collect_details.html', {
        'form': form,
        'course': course
    })

@login_required
def payment_instruction(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        tid = request.POST.get('transaction_id')
        if tid:
            enrollment, created = Enrollment.objects.get_or_create(
                user=request.user,
                course=course
            )
            enrollment.transaction_id = tid
            # Logic: is_paid stays False until Admin manually approves
            enrollment.save()
            return redirect('finalize_enrollment', enrollment_id=enrollment.id)

    return render(request, 'enrollments/payment_page.html', {'course': course})

@login_required
def finalize_enrollment(request, enrollment_id):
    # Security: Ensure only the owner of the enrollment can see this
    enrollment = get_object_or_404(
        Enrollment.objects.select_related('user', 'course'),
        id=enrollment_id,
        user=request.user
    )

    # If you haven't approved it yet, show a 'Pending' page instead of the receipt
    if not enrollment.is_paid:
        return render(request, 'enrollments/pending_verification.html', {'enrollment': enrollment})

    return render(request, 'enrollments/receipt.html', {'enrollment': enrollment})