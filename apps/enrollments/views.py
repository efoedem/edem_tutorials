import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrollment
from apps.courses.models import Course
from .forms import EnrollmentDetailsForm


@login_required
def initiate_enrollment(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Optional: Check if user is already enrolled and paid
    existing_enrollment = Enrollment.objects.filter(user=request.user, course=course, is_paid=True).first()
    if existing_enrollment:
        messages.info(request, "You are already enrolled in this course.")
        return redirect('course_list')

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
            # This ensures we don't create duplicate rows for the same user/course
            enrollment, created = Enrollment.objects.get_or_create(
                user=request.user,
                course=course
            )
            enrollment.transaction_id = tid
            # Important: Admin must manually set is_paid to True in the Django Admin panel
            enrollment.save()
            return redirect('finalize_enrollment', enrollment_id=enrollment.id)
        else:
            messages.error(request, "Please enter a valid Transaction ID.")

    return render(request, 'enrollments/payment_page.html', {'course': course})


@login_required
def finalize_enrollment(request, enrollment_id):
    # Security: Only allow the logged-in user to see their own enrollment
    enrollment = get_object_or_404(
        Enrollment.objects.select_related('user', 'course'),
        id=enrollment_id,
        user=request.user
    )

    # Logic: If admin hasn't approved yet, show the 'Pending' page
    if not enrollment.is_paid:
        return render(request, 'enrollments/pending_verification.html', {
            'enrollment': enrollment
        })

    # If approved, show the receipt/success page
    return render(request, 'enrollments/receipt.html', {
        'enrollment': enrollment
    })