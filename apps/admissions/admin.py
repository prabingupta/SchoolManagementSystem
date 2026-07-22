from django.contrib import admin
from django.utils.html import format_html
from .models import Program, AdmissionStep, AdmissionRequirement, Enquiry


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'age_range', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'short_description')
    prepopulated_fields = {}  # slug is auto-generated in model.save(), not user-edited


@admin.register(AdmissionStep)
class AdmissionStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title')
    ordering = ('step_number',)


@admin.register(AdmissionRequirement)
class AdmissionRequirementAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    """
    Admin for admission enquiries — the primary tool office staff
    will use daily to track and follow up on leads.

    Read-only on submitted fields (parent shouldn't have their
    original message edited), but status/notes are editable so
    staff can track follow-up progress without a separate CRM.
    """
    list_display = (
        'parent_name', 'student_name', 'phone', 'interested_grade',
        'status_badge', 'created_at'
    )
    list_filter = ('status', 'interested_grade', 'created_at')
    search_fields = ('parent_name', 'student_name', 'email', 'phone')
    readonly_fields = (
        'parent_name', 'student_name', 'email', 'phone',
        'current_school', 'interested_grade', 'preferred_visit_date',
        'message', 'created_at', 'updated_at'
    )
    list_editable = ()  # status is edited via detail page, not inline, to avoid accidental bulk changes
    ordering = ('-created_at',)

    fieldsets = (
        ("Submitted Information (read-only)", {
            'fields': (
                'parent_name', 'student_name', 'email', 'phone',
                'current_school', 'interested_grade',
                'preferred_visit_date', 'message'
            )
        }),
        ("Office Follow-Up", {
            'fields': ('status', 'admin_notes')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )

    STATUS_COLORS = {
        'new': '#3b82f6',
        'contacted': '#f59e0b',
        'visit_scheduled': '#8b5cf6',
        'enrolled': '#10b981',
        'closed': '#6b7280',
    }

    @admin.display(description="Status")
    def status_badge(self, obj):
        color = self.STATUS_COLORS.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
