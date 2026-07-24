from django.db import models
from apps.core.models import TimeStampedModel


class ContactSubmission(TimeStampedModel):
    """
    A message submitted through the public Contact page form.

    Kept deliberately separate from admissions.Enquiry — a contact
    submission is a general inquiry (e.g. a vendor, a general
    question, a complaint), while an Enquiry is specifically a
    parent exploring admission for a student. Merging them would
    force one model to carry fields irrelevant to half its rows
    (e.g. 'interested_grade' makes no sense for a vendor message).
    """
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.subject or 'No subject'}"


class FAQ(TimeStampedModel):
    """
    A single Frequently Asked Question, shown on the homepage
    FAQ section and/or a dedicated FAQ page.
    """
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class NewsletterSubscriber(TimeStampedModel):
    """
    Email captured from the footer newsletter signup.

    Deliberately minimal (just email + active flag) for v1 —
    this is a capture point, not a full campaign-management system.
    Future SMTP/email-marketing integration (Mailchimp, etc.) can
    read from this table without any schema changes.
    """
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email
