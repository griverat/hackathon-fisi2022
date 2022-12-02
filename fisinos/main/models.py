import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

# Create topics that can be suscribed by users


class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    suscribers = models.ManyToManyField(User, related_name="topics", blank=True)

    def __str__(self):
        return self.name


# Create announcements that can be suscribed by users by topics
# announcements can have multiple topics
# and can be suscribed by multiple users


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    topics = models.ManyToManyField(Topic, related_name="announcements")
    # users = models.ManyToManyField(User, related_name='announcements')
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.title

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def topics_list(self):
        # sort topics by name
        return ", ".join([topic.name for topic in self.topics.all().order_by("name")])

    def get_topics(self):
        return self.topics.all()


# Create users profile that can suscribe to announcements by topics
# users can be retrieved from the django auth user model
# users can have multiple topics suscribed


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, related_name="users")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# detect when a user logs in and has no user profile
@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    if not hasattr(user, "userprofile"):
        UserProfile.objects.create(user=user)
