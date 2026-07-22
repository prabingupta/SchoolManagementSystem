from django.db import models
from apps.core.models import TimeStampedModel


class SchoolStory(TimeStampedModel):
    """
    Singleton-style model holding the school's narrative content:
    Mission, Vision, and History/Story text shown on the About page.

    Kept as a single editable row (like SiteSettings) since a school
    has exactly one mission and one vision statement at any given time,
    unlike PrincipalMessage which benefits from historical records.
    """
    mission = models.TextField(help_text="The school's mission statement.")
    vision = models.TextField(help_text="The school's vision statement.")
    history = models.TextField(
        help_text="The school's founding story and journey, shown in the 'Our Story' section."
    )
    founded_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "School Story"
        verbose_name_plural = "School Story"

    def __str__(self):
        return "School Story (Mission, Vision & History)"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton, same pattern as SiteSettings
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass


class CoreValue(TimeStampedModel):
    """
    A single value card (e.g. Integrity, Excellence, Respect) shown
    in the 'Our Values' section of the About page.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Core Values"

    def __str__(self):
        return self.title


class TimelineEvent(TimeStampedModel):
    """
    A single milestone in the school's history timeline
    (e.g. 'Founded in 2010', 'First graduating batch in 2014').
    """
    year = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['year', 'order']

    def __str__(self):
        return f"{self.year} — {self.title}"


class Achievement(TimeStampedModel):
    """
    A school or student achievement/award shown in the
    'Why Parents Trust Us' or Achievements section.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    icon_class = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class TeacherProfile(TimeStampedModel):
    """
    Faculty directory entry, used for the 'Faculty Overview'
    section on the About page.

    Deliberately kept simple for now (no linked user account) —
    this is a public-facing directory model, not an authentication
    model. When the Teacher Portal is built later (per the
    'future extensions' architecture), this can be linked via a
    OneToOneField to a Django User without breaking this model's
    existing data.
    """
    full_name = models.CharField(max_length=150)
    designation = models.CharField(
        max_length=150,
        help_text="e.g. 'Senior Mathematics Teacher', 'Head of Science Department'"
    )
    subject_specialty = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to='staff/teachers/', blank=True, null=True)
    bio = models.TextField(blank=True)
    qualification = models.CharField(
        max_length=200,
        blank=True,
        help_text="e.g. 'M.Ed in Mathematics Education'"
    )
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.full_name} — {self.designation}"
