from django.conf.urls import url
from newsletter.views.newsletter_open import index as newsletter_open_index
from newsletter.views.newsletter_view import track_open
from newsletter.views.newsletter_view import index as index_newsletter
from newsletter.views.subscriber_view import delete as delete_subscriber
from newsletter.views.subscriber_view import index as index_subscriber

urlpatterns = [
    url(r'^$', index_newsletter, name='newsletter.index'),
    url(r'^track-open/(?P<track_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', track_open, name='track.open'),
    url(r'^subscribers/$', index_subscriber, name='subscribers.index'),
    url(r'^subscribers/delete/(?P<subscriber_id>\d+)/$', delete_subscriber, name='subscribers.delete'),
    url(r'^(?P<newsletter_id>\d+)/trackers/$', newsletter_open_index, name='newsletters.trackers.index'),
]
