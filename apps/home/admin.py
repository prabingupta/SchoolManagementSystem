from django.contrib import admin
from .models import HeroSlide, StatCounter, Highlight, PrincipalMessage


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    fieldsets = (
        ("Content", {
            'fields': ('title', 'subtitle', 'background_image')
        }),
        ("Primary Call To Action", {
            'fields': ('primary_cta_text', 'primary_cta_link')
        }),
        ("Secondary Call To Action", {
            'fields': ('secondary_cta_text', 'secondary_cta_link')
        }),
        ("Display Settings", {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(StatCounter)
class StatCounterAdmin(admin.ModelAdmin):
    list_display = ('label', 'number', 'suffix', 'order')
    list_editable = ('number', 'suffix', 'order')
    ordering = ('order',)


@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(PrincipalMessage)
class PrincipalMessageAdmin(admin.ModelAdmin):
    list_display = ('principal_name', 'designation', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
