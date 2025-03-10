from __future__ import print_function
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.utils import timezone
from newsletter.forms import NewsletterForm
from newsletter.managers import NewsLetterOpenManager, NewsLetterManager
from newsletter_service import settings


def index(request):
    form = NewsletterForm()
    newsletters = NewsLetterManager.get_newsletters()

    return render(request, 'pages/newsletter/index.html', {'form': form, 'newsletters': newsletters})

def track_open(request, track_id):
    NewsLetterOpenManager.update_newsletter_open_by_track_id(track_id, opened=True, opened_at=timezone.now())
    transparent_img = '{}/1x1.png'.format(settings.MEDIA_ROOT)

    def file_iterator(file_name, chunk_size=1024):
        with open(file_name, 'rb') as fp:
            while True:
                chunk = fp.read(chunk_size)

                if not chunk:
                    break
                yield chunk

    response = StreamingHttpResponse(file_iterator(transparent_img), content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format('1x1.png')

    return response
