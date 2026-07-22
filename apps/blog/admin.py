from django.contrib import admin
from .models import BlogCategory, BlogTag, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'status', 'is_featured',
        'view_count', 'published_at'
    )
    list_editable = ('status', 'is_featured')
    list_filter = ('status', 'category', 'is_featured', 'tags')
    search_fields = ('title', 'excerpt', 'content')
    filter_horizontal = ('tags',)
    readonly_fields = ('view_count', 'published_at')
    date_hierarchy = 'published_at'

    fieldsets = (
        ("Content", {
            'fields': ('title', 'category', 'tags', 'featured_image', 'excerpt', 'content', 'author_name')
        }),
        ("Publishing", {
            'fields': ('status', 'is_featured', 'published_at', 'view_count')
        }),
        ("SEO", {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
