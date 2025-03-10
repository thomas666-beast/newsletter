import logging
import uuid
from smtplib import SMTPException
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from newsletter.forms import NewsletterForm
from newsletter.managers import NewsLetterOpenManager, NewsLetterManager
from newsletter.models import Newsletter, Subscriber
from newsletter_service.settings import DOMAIN_NAME, DEFAULT_FROM_EMAIL
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

@csrf_exempt  # Only for testing
@require_POST
def store(request):
        form = NewsletterForm(request.POST)

        if form.is_valid():
            newsletter = form.save()

            if newsletter.send_time:
                send_newsletter.apply_async((newsletter.id,), eta=newsletter.send_time)
            else:
                send_newsletter.apply_async((newsletter.id,))

            return JsonResponse({'success': True, 'message': _('newsletter_registered')})

        return JsonResponse({'success': False, 'errors': form.errors})


@shared_task
def send_newsletter(newsletter_id):
    newsletter = NewsLetterManager.get_newsletter_by_id(newsletter_id)

    if not newsletter:
        return {'success': False, 'message': _('newsletter_id_not_found').format(newsletter_id)}

    newsletter_open_data = []
    subscribers = Subscriber.objects.iterator()

    if not newsletter.send_time:
        newsletter.send_time = timezone.now()
        newsletter.save()

    for subscriber in subscribers:
        subscriber_content = newsletter.html_content.format(
            firstname=subscriber.firstname,
            lastname=subscriber.lastname,
            birthday=subscriber.birthday.strftime('%Y-%m-%d') if subscriber.birthday else 'N/A'
        )
        track_id = uuid.uuid4()
        tracking_image = '<img src="{}" width="1" height="1" style="display:none;" />'.format(
            DOMAIN_NAME +  reverse('track.open', kwargs={'track_id': track_id}),
        )
        full_content = subscriber_content + tracking_image

        if send_email(subscriber.email, newsletter.subject, full_content):
            newsletter_open = NewsLetterOpenManager.create_newsletter_open_data(
                subscriber=subscriber,
                newsletter=newsletter,
                track_id=track_id
            )
            newsletter_open_data.append(newsletter_open)

    with transaction.atomic():
        NewsLetterOpenManager.bulk_create(newsletter_open_data)

    return {'status': 'completed', 'total_sent': len(newsletter_open_data)}


def send_email(recipient, subject, html_message):
    try:
        send_mail(
            subject=subject,
            message='',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
            html_message=html_message
        )

        return True
    except BadHeaderError:
        logger.error("Invalid header found when sending email to {}.".format(recipient))
    except SMTPException as e:
        logger.error("SMTP error occurred while sending email to {}: {}".format(recipient, str(e)))
    except Exception as e:
        logger.error("Failed to send email to {}: {}".format(recipient, str(e)))

    return False