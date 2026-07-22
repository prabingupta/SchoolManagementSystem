from django.db import models
from apps.core.models import TimeStampedModel, SlugModel


class ServiceCategory(models.TextChoices):
    """
    Fixed categories for organizing services/facilities into
    the sections outlined in the spec (Extra Curricular,
    Transportation, Library, etc.).

    Using TextChoices instead of a separate model/table here
    because these categories are a fixed, small, rarely-changing
    set defined by the school's operational structure — not
    user-generated content that needs its own admin CRUD.
    """
    ACADEMIC = 'academic', 'Academic Support'
    EXTRA_CURRICULAR = 'extra_curricular', 'Extra Curricular'
    TRANSPORTATION = 'transportation', 'Transportation'
    HOSTEL = 'hostel', 'Hostel'
    LIBRARY = 'library', 'Library'
    LABORATORY = 'laboratory', 'Laboratories'
    COMPUTER_LAB = 'computer_lab', 'Computer Lab'
    SPORTS = 'sports', 'Sports'
    COUNSELLING = 'counselling', 'Counselling'
    DIGITAL_LEARNING = 'digital_learning', 'Digital Learning'


class Service(TimeStampedModel, SlugModel):
    """
    A single facility/service offered by the school, shown on
    the Services page grouped by category.
    """
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=ServiceCategory.choices)
    short_description = models.CharField(max_length=255)
    full_description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True)
    featured_image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    def get_slug_source(self):
        return self.name


class ServiceGalleryImage(TimeStampedModel):
    """
    Supporting images for a specific service (e.g. multiple
    photos of the library, computer lab, sports facilities).

    Separate from the main 'gallery' app deliberately — these
    images are tightly coupled to a specific service's detail
    page, whereas the 'gallery' app is the general-purpose,
    freely browsable school photo gallery. Mixing them would
    force awkward filtering logic in both places.
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='services/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.service.name}"
