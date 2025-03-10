from django.shortcuts import render
from newsletter.models import NewsletterOpen


def index(request, newsletter_id):
    newsletters_open = NewsletterOpen.objects.filter(newsletter_id=newsletter_id)

    return render(request, 'pages/newsletter/trackers/index.html', {'newsletters_open': newsletters_open})
