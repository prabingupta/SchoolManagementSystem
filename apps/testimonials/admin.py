from django.contrib import admin
from django.utils.html import format_html
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'star_display', 'is_featured', 'is_active', 'order')
    list_editable = ('is_featured', 'is_active', 'order')
    list_filter = ('role', 'is_featured', 'is_active')
    search_fields = ('name', 'message')

    @admin.display(description="Rating")
    def star_display(self, obj):
        full_stars = '★' * obj.rating
        empty_stars = '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color:#f59e0b; letter-spacing:2px;">{}{}</span>',
            full_stars, empty_stars
        )
