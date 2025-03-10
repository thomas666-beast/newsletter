from newsletter.models import Subscriber, Newsletter, NewsletterOpen


class SubscriberManager(object):

    @classmethod
    def get_subscribers(cls):
        return Subscriber.objects.order_by('-created_on').all()

    @classmethod
    def store_subscriber(cls, **kwargs):
        subscriber = Subscriber.objects.create(**kwargs)

        return subscriber

    @classmethod
    def get_subscriber_by_id(cls, subscriber_id):

        try:
            subscriber = Subscriber.objects.get(id=subscriber_id)
        except Subscriber.DoesNotExist:
            return None

        return subscriber

    @classmethod
    def get_subscriber_by_email(cls, email):
        try:
            subscriber = Subscriber.objects.get(email=email)
        except Subscriber.DoesNotExist:
            return None

        return subscriber

    @classmethod
    def update_subscriber(cls, subscriber_id, **kwargs):
        subscriber = cls.get_subscriber_by_id(subscriber_id)

        if subscriber is None:
            return False

        for key, value in kwargs.items():
            subscriber.__dict__[key] = value

        subscriber.save()

        return True

    @classmethod
    def delete_subscriber(cls, subscriber_id):
        subscriber = cls.get_subscriber_by_id(subscriber_id)
        if subscriber is None:
            return None

        subscriber.delete()

        return True

class NewsLetterManager(object):
    @classmethod
    def get_newsletters(cls):
        return Newsletter.objects.order_by('-created_on').all()

    @classmethod
    def store_newsletter(cls, **kwargs):
        newsletter = Newsletter.objects.create(**kwargs)

        return newsletter

    @classmethod
    def get_newsletter_by_id(cls, newsletter_id):
        try:
            newsletter = Newsletter.objects.get(id=newsletter_id)
        except Newsletter.DoesNotExist:
            return None

        return newsletter

    @classmethod
    def update_newsletter(cls, newsletter_id, **kwargs):
        newsletter = cls.get_newsletter_by_id(newsletter_id)

        if newsletter is None:
            return False

        for key, value in kwargs.items():
            newsletter.__dict__[key] = value

        newsletter.save()

        return True

    @classmethod
    def delete_newsletter(cls, newsletter_id):
        newsletter = cls.get_newsletter_by_id(newsletter_id)

        if newsletter is None:
            return False

        newsletter.delete()

        return True

class NewsLetterOpenManager(object):
    @classmethod
    def get_newsletters_open(cls, filter_by = None):
        return NewsletterOpen.objects.all()

    @classmethod
    def store_newsletter_open(cls, **kwargs):
        newsletter = NewsletterOpen.objects.create(**kwargs)

        return newsletter

    @classmethod
    def get_newsletter_open_by_id(cls, id):
        try:
            newsletter_open = NewsletterOpen.objects.get(id=id)
        except NewsletterOpen.DoesNotExist:
            return None

        return newsletter_open

    @classmethod
    def get_newsletter_open_by_track_id(cls, track_id):
        try:
            newsletter_open = NewsletterOpen.objects.get(track_id=track_id)
        except NewsletterOpen.DoesNotExist:
            return None

        return newsletter_open

    @classmethod
    def update_newsletter_open_by_id(cls, newsletter_open_id, **kwargs):
        newsletter_open = cls.get_newsletter_open_by_id(newsletter_open_id)

        if newsletter_open is None:
            return False

        for key, value in kwargs.items():
            newsletter_open.__dict__[key] = value

        newsletter_open.save()

        return True

    @classmethod
    def update_newsletter_open_by_track_id(cls, track_id, **kwargs):
        newsletter_open = cls.get_newsletter_open_by_track_id(track_id)

        if newsletter_open is None:
            return False

        if not newsletter_open.opened:
            for key, value in kwargs.items():
                newsletter_open.__dict__[key] = value

            newsletter_open.save()

        return True

    @classmethod
    def create_newsletter_open_data(cls, subscriber, newsletter, track_id):
        return {
            'subscriber': subscriber,
            'newsletter': newsletter,
            'track_id': track_id,
        }

    @classmethod
    def bulk_create(cls, newsletter_open_data):
        # Assuming you have a NewsletterOpen model
        NewsletterOpen.objects.bulk_create([
            NewsletterOpen(**data) for data in newsletter_open_data
        ])