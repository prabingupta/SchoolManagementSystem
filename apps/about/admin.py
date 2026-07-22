from django.contrib import admin
from .models import SchoolStory, CoreValue, TimelineEvent, Achievement, TeacherProfile


@admin.register(SchoolStory)
class SchoolStoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Mission & Vision", {
            'fields': ('mission', 'vision')
        }),
        ("History", {
            'fields': ('founded_year', 'history')
        }),
    )

    def has_add_permission(self, request):
        return not SchoolStory.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'order')
    list_editable = ('order',)
    ordering = ('year', 'order')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'designation', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('full_name', 'designation', 'subject_specialty')
    fieldsets = (
        ("Personal Info", {
            'fields': ('full_name', 'photo')
        }),
        ("Professional Info", {
            'fields': ('designation', 'subject_specialty', 'qualification', 'years_of_experience', 'bio')
        }),
        ("Display Settings", {
            'fields': ('is_active', 'order')
        }),
    )
