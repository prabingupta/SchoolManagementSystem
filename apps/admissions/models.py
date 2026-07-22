from django.db import models
from apps.core.models import TimeStampedModel, SlugModel


class Program(TimeStampedModel, SlugModel):
    """
    An academic program/grade level offered by the school
    (e.g. 'Early Childhood Development', 'Primary Level', 'Secondary Level').

    Used on both the Admissions page and Services page, since
    programs are simultaneously an academic offering and an
    admissions category.
    """
    name = models.CharField(max_length=150)
    short_description = models.CharField(
        max_length=255,
        help_text="One-line summary shown on cards/previews."
    )
    full_description = models.TextField()
    age_range = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. '3-5 years', 'Grade 1-5'"
    )
    icon_class = models.CharField(max_length=50, blank=True)
    featured_image = models.ImageField(upload_to='programs/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_slug_source(self):
        return self.name


class AdmissionStep(TimeStampedModel):
    """
    A single step in the admission process, displayed as a
    numbered timeline/process flow on the Admissions page
    (e.g. Step 1: Submit Enquiry, Step 2: Campus Visit, Step 3: Assessment).
    """
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class AdmissionRequirement(TimeStampedModel):
    """
    A single required document/item for admission
    (e.g. 'Birth Certificate', 'Previous School Transfer Certificate').
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Enquiry(TimeStampedModel):
    """
    Admission enquiry submitted through the public enquiry form.

    This is the core lead-capture model referenced in the original
    spec's 'Consultation / Enquiry Form' section. Stored in the
    database now; architecture leaves room for:
      - future SMTP notification to admin on save (via Django signals
        or in the view, added when email is configured)
      - future SMS gateway integration (same pattern)
      - a status field so admin staff can track follow-up without
        needing a separate CRM
    """

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('visit_scheduled', 'Visit Scheduled'),
        ('enrolled', 'Enrolled'),
        ('closed', 'Closed'),
    ]

    parent_name = models.CharField(max_length=150)
    student_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    current_school = models.CharField(max_length=200, blank=True)
    interested_grade = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries',
        help_text="The program/grade the parent is interested in."
    )
    preferred_visit_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True, help_text="Additional questions from the parent.")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes for staff follow-up (not visible to the parent)."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.parent_name} — {self.student_name} ({self.get_status_display()})"
