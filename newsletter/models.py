from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils.translation import gettext as _

class Subscriber(models.Model):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': _('email_already_exists'),
            'required': _('required'),
            'invalid': _('invalid_email'),
        }
    )

    firstname = models.CharField(
        max_length=100,
        error_messages={
            'required': _('required'),
        }
    )
    lastname = models.CharField(
        max_length=100,
        error_messages={
            'required': _('required'),
        }
    )
    birthday = models.DateField(error_messages={'required': _('required')})
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class Newsletter(models.Model):
    subject = models.CharField(max_length=100, error_messages={'required': _('required')})
    html_content = models.TextField(error_messages={'required': _('required')})
    send_time = models.DateTimeField(null=True, blank=True, error_messages={'invalid': _('invalid_date_time')})
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class NewsletterOpen(models.Model):
    track_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('subscriber', 'newsletter')

    def __str__(self):
        return "{} opened {}: {} (Track ID: {})".format(self.subscriber.email, self.newsletter.subject, self.opened, self.track_id)