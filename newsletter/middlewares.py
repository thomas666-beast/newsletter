from django.utils import translation

class LanguageSwitcherMiddleware(object):
    def process_request(self, request):
        # Set the default language to Russian
        translation.activate('ru')
        request.LANGUAGE_CODE = 'ru'

