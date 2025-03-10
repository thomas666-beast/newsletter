from django.conf.urls import url

from newsletter.views.api.newsletter_view_api import store as store_newsletter
from newsletter.views.api.subscriber_view_api import store as store_subscriber

urlpatterns = [
    url(r'^store/$', store_newsletter, name='api.newsletter.store'),
    url(r'^subscribers/store/$', store_subscriber, name='api.subscribers.store'),
]
