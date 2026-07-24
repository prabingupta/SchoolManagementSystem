from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.core.models import TimeStampedModel


class Role(models.TextChoices):
    """
    Fixed set of portal roles this architecture is prepared for.
    ADMIN covers school office staff managing content via Django Admin
    (already working today). STUDENT, TEACHER, and PARENT are reserved
    for the future portal login system referenced in the project spec.
    """
    ADMIN = 'admin', 'Admin / Staff'
    TEACHER = 'teacher', 'Teacher'
    STUDENT = 'student', 'Student'
    PARENT = 'parent', 'Parent'


class Profile(TimeStampedModel):
    """
    Extends Django's built-in User model via a OneToOneField,
    rather than replacing it with a custom User model.

    A Profile row is auto-created for every User via the signal
    below, so this never needs to be manually created.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='accounts/profiles/', blank=True, null=True)

    linked_teacher_profile = models.ForeignKey(
        'about.TeacherProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_accounts',
        help_text="Reserved for future Teacher Portal — links this login to a public faculty profile."
    )

    class Meta:
        verbose_name = "User Profile"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Ensures every Django User automatically has a Profile.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
