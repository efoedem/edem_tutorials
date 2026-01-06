import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from urllib.parse import quote
from .models import Enrollment


# 1. Enhanced Export Function including Transaction ID
def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_enrollments_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Student Name',
        'Index Number',
        'WhatsApp',
        'Course',
        'Transaction ID',
        'Paid Status',
        'Date Enrolled'
    ])

    for obj in queryset:
        writer.writerow([
            obj.user.get_full_name() or obj.user.username,
            obj.user.index_number,
            obj.user.whatsapp_number,
            obj.course.title,
            obj.transaction_id,
            "Paid" if obj.is_paid else "Unpaid",
            obj.enrolled_at.strftime("%Y-%m-%d %H:%M")
        ])
    return response


export_to_excel.short_description = "🚀 Export Selected to Excel"


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'get_student_name',
        'get_index_number',
        'get_whatsapp',
        'course',
        'transaction_id',
        'is_paid',
        'send_whatsapp_btn',  # <--- Added the Notify Button here
        'enrolled_at'
    )

    list_editable = ('is_paid',)
    actions = [export_to_excel]
    list_filter = ('is_paid', 'course', 'enrolled_at')
    search_fields = ('user__username', 'user__index_number', 'transaction_id')

    # Registering the Sidebar JS and CSS
    class Media:
        js = ('admin/js/sidebar_toggle.js',)
        css = {'all': ('admin/css/custom_admin.css',)}

    # --- NEW: WhatsApp Notification Logic ---
    def send_whatsapp_btn(self, obj):
        if not obj.user.whatsapp_number:
            return "No Number"

        # Customize your message here
        message = (
            f"Hello {obj.user.get_full_name() or obj.user.username}, "
            f"your payment for {obj.course.title} (ID: {obj.transaction_id}) "
            f"has been VERIFIED. You can now download your receipt. "
            f" You're officially part of EDEM TUTORIAL.....Thank you!"
        )

        # Formats number for Ghana (converts 0... to 233...)
        phone = obj.user.whatsapp_number
        if phone.startswith('0'):
            phone = '233' + phone[1:]

        url = f"https://wa.me/{phone}?text={quote(message)}"

        return format_html(
            '<a class="button" href="{}" target="_blank" style="background-color: #25D366; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 10px;">NOTIFY WA</a>',
            url
        )

    send_whatsapp_btn.short_description = 'WhatsApp Notify'

    # --- Helper methods for Admin display ---
    def get_student_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    get_student_name.short_description = 'Student Name'

    def get_index_number(self, obj):
        return obj.user.index_number

    get_index_number.short_description = 'Index No'

    def get_whatsapp(self, obj):
        return obj.user.whatsapp_number

    get_whatsapp.short_description = 'WhatsApp'

# NO admin.site.register(Enrollment) needed due to @admin.register decorator