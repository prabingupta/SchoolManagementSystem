from django.db import models
from django.urls import reverse
from apps.core.models import TimeStampedModel, SlugModel, SEOModel


class BlogCategory(TimeStampedModel, SlugModel):
    """
    Post category (e.g. 'School News', 'Admission Updates',
    'Learning Tips', 'Announcements', 'Events').
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_slug_source(self):
        return self.name


class BlogTag(models.Model):
    """
    Lightweight tag for cross-cutting topics, separate from
    category (a post has one category but can have many tags —
    e.g. category 'School News' with tags 'Sports', 'Achievement').
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogPost(TimeStampedModel, SlugModel, SEOModel):
    """
    A single blog post/news article/announcement.

    Inherits TimeStampedModel (created_at/updated_at), SlugModel
    (auto slug from title), and SEOModel (meta fields) — this is
    the model that benefits most from all three abstract base
    classes, since blog content is exactly what search engines
    index and what the 'Recent/Popular Posts' features query on.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.PROTECT, related_name='posts'
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='posts')

    featured_image = models.ImageField(upload_to='blog/')
    excerpt = models.CharField(
        max_length=300,
        help_text="Short summary shown in post previews and search results."
    )
    content = models.TextField()

    author_name = models.CharField(max_length=150, default="River Queens School")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(
        null=True, blank=True,
        help_text="Set automatically when status changes to Published, if left blank."
    )

    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Incremented each time the post is viewed; powers the 'Popular Posts' section."
    )
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def get_slug_source(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        from django.utils import timezone
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
