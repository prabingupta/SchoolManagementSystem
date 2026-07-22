from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.

    Every content model in this project (Blog, Testimonial,
    Event, GalleryItem, TeacherProfile, etc.) inherits this
    instead of redefining these two fields repeatedly.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """
    Abstract base model that provides standard SEO fields.

    Any page-like or content model (BlogPost, Program, Event)
    inherits this so every piece of content is search-engine
    optimized by default, without repeating these fields
    across 6+ models.
    """
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Recommended: 50-60 characters for optimal display in search results."
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Recommended: 150-160 characters for optimal display in search results."
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords (optional, low SEO weight but harmless)."
    )

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """
    Abstract base model that provides an auto-generated,
    unique slug field derived from a 'title' or 'name'
    field on the child model.

    Child models must implement a `get_slug_source()` method
    returning the string to slugify (e.g. self.title).
    """
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    def get_slug_source(self):
        raise NotImplementedError(
            "Models using SlugModel must implement get_slug_source()."
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.get_slug_source())
            slug = base_slug
            counter = 1
            model_class = self.__class__
            while model_class.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class SiteSettings(TimeStampedModel):
    """
    Singleton-style model holding sitewide configuration:
    school name, tagline, logo, contact details, social links.

    Enforced as a singleton via save() override — there should
    only ever be one row. Editable through Django Admin so
    non-technical staff can update site info without a
    developer touching code.
    """
    school_name = models.CharField(max_length=200, default="River Queens School")
    tagline = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short phrase shown near the logo, e.g. 'Nurturing Minds, Shaping Futures'."
    )
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)

    email = models.EmailField(blank=True)
    phone_primary = models.CharField(max_length=20, blank=True)
    phone_secondary = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    google_maps_embed_url = models.URLField(blank=True)

    office_hours = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g. 'Sunday - Friday: 9:00 AM - 4:00 PM'"
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.school_name

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # prevent accidental deletion of the singleton row


class SocialLink(TimeStampedModel):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter / X'),
        ('linkedin', 'LinkedIn'),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_platform_display()}"
