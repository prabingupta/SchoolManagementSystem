from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.core.models import TimeStampedModel


class Testimonial(TimeStampedModel):
    """
    A single testimonial/review from a parent, student, alumnus,
    or teacher, shown in the homepage preview and the dedicated
    Testimonials page slider.
    """

    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('teacher', 'Teacher'),
    ]

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    role_detail = models.CharField(
        max_length=150,
        blank=True,
        help_text="Optional extra context, e.g. 'Parent of Grade 5 student', 'Class of 2020'"
    )
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        help_text="Rating out of 5 stars."
    )
    message = models.TextField()

    is_featured = models.BooleanField(
        default=False,
        help_text="Featured testimonials appear in the homepage preview section."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive testimonials are hidden from the site without deleting them."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_role_display()}) — {self.rating}★"
