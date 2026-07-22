from django.db import models
from apps.core.models import TimeStampedModel


class HeroSlide(TimeStampedModel):
    """
    A single slide in the homepage hero section.

    Modeled as multiple slides (not a single hero) so the school
    can rotate between different messages/campaigns (e.g. admissions
    open, sports day highlight, exam results) without a developer
    touching templates — content editors just add/reorder rows here.
    """
    title = models.CharField(
        max_length=200,
        help_text="Main headline, e.g. 'Nurturing Tomorrow's Leaders Today'"
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        help_text="Supporting line under the headline."
    )
    background_image = models.ImageField(upload_to='hero/')

    primary_cta_text = models.CharField(max_length=50, default="Apply for Admission")
    primary_cta_link = models.CharField(max_length=255, default="/admissions/")

    secondary_cta_text = models.CharField(max_length=50, default="Contact Us", blank=True)
    secondary_cta_link = models.CharField(max_length=255, default="/contact/", blank=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class StatCounter(TimeStampedModel):
    """
    Animated statistic shown in the hero/stats bar
    (e.g. '15+ Years of Excellence', '1200+ Students', '98% Pass Rate').

    Stored as structured data (number + suffix + label) rather than
    a single text field, so the frontend JS counter animation can
    animate the numeric part precisely regardless of content.
    """
    number = models.PositiveIntegerField(help_text="e.g. 15, 1200, 98")
    suffix = models.CharField(max_length=10, blank=True, help_text="e.g. '+', '%'")
    label = models.CharField(max_length=100, help_text="e.g. 'Years of Excellence'")
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional icon identifier used by the template, e.g. 'icon-graduation-cap'"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.number}{self.suffix} {self.label}"


class Highlight(TimeStampedModel):
    """
    A single card in the 'Why Choose River Queens School' section.
    """
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon identifier used by the template, e.g. 'icon-book-open'"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class PrincipalMessage(TimeStampedModel):
    """
    Singleton-style model for the Principal's welcome message
    shown on the homepage and About page.

    Not enforced as a strict singleton like SiteSettings, because
    a school may want to archive a past principal's message when
    leadership changes rather than being forced to overwrite it.
    Instead, we use `is_active` so only one is displayed at a time,
    enforced in the view/query layer, not the model layer.
    """
    principal_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=100, default="Principal")
    photo = models.ImageField(upload_to='staff/principal/', blank=True, null=True)
    message = models.TextField()
    is_active = models.BooleanField(
        default=True,
        help_text="Only one active message is shown at a time."
    )

    class Meta:
        verbose_name = "Principal's Message"
        verbose_name_plural = "Principal's Messages"

    def __str__(self):
        return f"{self.principal_name} ({'Active' if self.is_active else 'Archived'})"
