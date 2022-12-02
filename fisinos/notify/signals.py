from django.db.models.signals import m2m_changed
from django.core.mail import send_mail

from main.models import Announcement, UserProfile

def send_post_mail(sender, instance, action, **kwargs):
    if action == "post_add":
        # send mail to all users suscribed to the announcement topics
        # if the announcement has multiple topics, send mail to all users suscribed to any of the topics
        # without sending multiple mails to the same user
        # get all users suscribed to the announcement topics
        users = set()
        for topic in instance.topics.all():
            users.update(topic.users.all())
        # send mail to all users
        for user in users:
            send_mail(
                'Nuevo Anuncio: ' + instance.title,
                instance.description,
                'notify@fisinos.lol',
                [user.user.email],
                fail_silently=False,
            )

m2m_changed.connect(send_post_mail, sender=Announcement.topics.through)