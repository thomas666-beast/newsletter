from django.test import TestCase
from django.utils import timezone

from newsletter.models import Subscriber, Newsletter, NewsletterOpen


class SubscriberModelTest(TestCase):

    def setUp(self):
        self.subscriber = Subscriber.objects.create(
            email='test@example.com',
            firstname='Boris',
            lastname='Yeltsin',
            birthday='1990-01-01'
        )

    def test_subscriber_creation(self):
        self.assertEqual(self.subscriber.email, 'test@example.com')
        self.assertEqual(self.subscriber.firstname, 'Boris')
        self.assertEqual(self.subscriber.lastname, 'Yeltsin')
        self.assertIsNotNone(self.subscriber.created_on)
        self.assertIsNotNone(self.subscriber.updated_on)

    def test_unique_email(self):
        with self.assertRaises(Exception):
            Subscriber.objects.create(
                email='test@example.com',
                firstname='Nikita',
                lastname='Khrushchev',
                birthday='1992-02-02'
            )

    def test_str_method(self):
        self.assertEqual(str(self.subscriber), 'test@example.com')


class NewsletterModelTest(TestCase):

    def setUp(self):
        self.newsletter = Newsletter.objects.create(
            subject='Weekly Update',
            html_content='<h1>Content</h1>',
            send_time=timezone.now()
        )

    def test_newsletter_creation(self):
        self.assertEqual(self.newsletter.subject, 'Weekly Update')
        self.assertEqual(self.newsletter.html_content, '<h1>Content</h1>')
        self.assertIsNotNone(self.newsletter.created_on)
        self.assertIsNotNone(self.newsletter.updated_on)

    def test_str_method(self):
        self.assertEqual(str(self.newsletter), 'Weekly Update')

class NewsletterOpenModelTest(TestCase):

    def setUp(self):
        self.subscriber = Subscriber.objects.create(
            email='test@example.com',
            firstname='John',
            lastname='Doe',
            birthday='1990-01-01'
        )
        self.newsletter = Newsletter.objects.create(
            subject='Weekly Update',
            html_content='<h1>Content</h1>',
            send_time=None
        )

    def test_newsletter_open_creation_with_track_id(self):
        newsletter_open = NewsletterOpen.objects.create(
            subscriber=self.subscriber,
            newsletter=self.newsletter,
            opened=True,
            opened_at=timezone.now()
        )
        self.assertIsNotNone(newsletter_open.track_id)  # Check that track_id is generated
        self.assertEqual(newsletter_open.subscriber, self.subscriber)
        self.assertEqual(newsletter_open.newsletter, self.newsletter)
        self.assertTrue(newsletter_open.opened)

    def test_unique_together_constraint(self):
        NewsletterOpen.objects.create(
            subscriber=self.subscriber,
            newsletter=self.newsletter,
            opened=True,
            opened_at=timezone.now()
        )
        with self.assertRaises(Exception):
            NewsletterOpen.objects.create(
                subscriber=self.subscriber,
                newsletter=self.newsletter,
                opened=False
            )
