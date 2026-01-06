from django.urls import path
from . import views

urlpatterns = [
    # 1. Start here (Collect Details)
    path('start/<int:course_id>/', views.initiate_enrollment, name='initiate_enrollment'),

    # 2. Payment Page (Enter Transaction ID)
    path('payment/<int:course_id>/', views.payment_instruction, name='payment_instruction'),

    # 3. Receipt Page (Success)
    path('receipt/<int:enrollment_id>/', views.finalize_enrollment, name='finalize_enrollment'),
]