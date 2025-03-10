from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from newsletter.forms import SubscriberForm
from newsletter.managers import SubscriberManager


@require_GET
def index(request):
    subscribers = SubscriberManager.get_subscribers()
    form = SubscriberForm()

    return render(request, 'pages/subscribers/index.html', {'subscribers': subscribers, 'form' : form})

def create(request):
    form = SubscriberForm()

    return render(request, 'pages/subscribers/create.html', {'form': form})

@require_POST
def delete(request, subscriber_id):
    SubscriberManager.delete_subscriber(subscriber_id)

    return redirect('subscribers.index')
