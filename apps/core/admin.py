from django.contrib import admin
from .models import SiteSettings, SocialLink


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Custom admin for the SiteSettings singleton.

    We disable 'Add' once a row exists (since save() enforces
    pk=1 anyway, this just keeps the admin UI honest — no
    'Add another' button tempting a staff member into confusion),
    and we disable delete entirely to protect the singleton.
    """
    fieldsets = (
        ("Identity", {
            'fields': ('school_name', 'tagline', 'logo', 'favicon')
        }),
        ("Contact Information", {
            'fields': ('email', 'phone_primary', 'phone_secondary', 'address', 'office_hours')
        }),
        ("Map", {
            'fields': ('google_maps_embed_url',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('platform', 'is_active')
