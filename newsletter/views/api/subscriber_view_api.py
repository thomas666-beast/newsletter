from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from newsletter.forms import SubscriberForm
from django.utils.translation import gettext as _


@csrf_exempt  # Only for testing
@require_POST
def store(request):
    form = SubscriberForm(request.POST)

    if form.is_valid():
        form.save()

        return JsonResponse({'success': True, 'message': _('subscriber_added!')})

    return JsonResponse({'success': False, 'errors': form.errors})
