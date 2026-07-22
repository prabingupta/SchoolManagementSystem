from django.db import models
from apps.core.models import TimeStampedModel, SlugModel


class GalleryCategory(TimeStampedModel, SlugModel):
    """
    A gallery category/album (e.g. 'Sports Day 2026', 'Annual Function',
    'Campus Facilities', 'Cultural Program').

    Modeled as its own table (not TextChoices, unlike ServiceCategory)
    because gallery categories are genuinely open-ended and
    event-driven — new albums get created every time the school
    holds an event, which staff should be able to do without a
    developer adding a new choice to a fixed list.
    """
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True, null=True)
    event_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-event_date', 'order']
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name

    def get_slug_source(self):
        return self.name


class GalleryImage(TimeStampedModel):
    """
    A single photo within a gallery category/album.
    """
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='gallery/photos/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Describes the image for screen readers and SEO (accessibility requirement)."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.category.name} — {self.caption or 'Untitled'}"
