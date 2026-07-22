from django.contrib import admin
from .models import GalleryCategory, GalleryImage


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3
    fields = ('image', 'caption', 'alt_text', 'order')


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    inlines = [GalleryImageInline]
