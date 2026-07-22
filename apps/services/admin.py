from django.contrib import admin
from .models import Service, ServiceGalleryImage


class ServiceGalleryImageInline(admin.TabularInline):
    """
    Inline editor so staff can manage a service's supporting
    photos directly from the Service edit page, instead of
    navigating to a separate model list.
    """
    model = ServiceGalleryImage
    extra = 1
    fields = ('image', 'caption', 'order')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'short_description')
    inlines = [ServiceGalleryImageInline]
    fieldsets = (
        ("Content", {
            'fields': ('name', 'category', 'short_description', 'full_description', 'featured_image', 'icon_class')
        }),
        ("Display Settings", {
            'fields': ('is_active', 'order')
        }),
    )
