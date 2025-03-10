import uuid

from django.test import TestCase
from django.utils import timezone

from newsletter.managers import SubscriberManager, NewsLetterManager, NewsLetterOpenManager
from newsletter.models import Newsletter, Subscriber, NewsletterOpen


class SubscriberManagerTest(TestCase):

    def setUp(self):
        self.subscriber_data = {
            'email': 'test@example.com',
            'firstname': 'John',
            'lastname': 'Doe',
            'birthday': '1990-01-01'
        }
        self.subscriber = SubscriberManager.store_subscriber(**self.subscriber_data)

    def test_store_subscriber(self):
        self.assertIsNotNone(self.subscriber)
        self.assertEqual(self.subscriber.email, self.subscriber_data['email'])

    def test_get_subscriber_by_id(self):
        retrieved_subscriber = SubscriberManager.get_subscriber_by_id(self.subscriber.id)
        self.assertEqual(retrieved_subscriber, self.subscriber)

    def test_get_subscriber_by_email(self):
        retrieved_subscriber = SubscriberManager.get_subscriber_by_email(self.subscriber_data['email'])
        self.assertEqual(retrieved_subscriber, self.subscriber)

    def test_update_subscriber(self):
        new_data = {'firstname': 'Jane', 'lastname': 'Smith'}
        result = SubscriberManager.update_subscriber(self.subscriber.id, **new_data)
        self.assertTrue(result)
        self.subscriber.refresh_from_db()
        self.assertEqual(self.subscriber.firstname, 'Jane')
        self.assertEqual(self.subscriber.lastname, 'Smith')

    def test_update_non_existent_subscriber(self):
        result = SubscriberManager.update_subscriber(999, firstname='NewName')
        self.assertFalse(result)

    def test_delete_subscriber(self):
        result = SubscriberManager.delete_subscriber(self.subscriber.id)
        self.assertTrue(result)
        self.assertIsNone(SubscriberManager.get_subscriber_by_id(self.subscriber.id))

    def test_delete_non_existent_subscriber(self):
        result = SubscriberManager.delete_subscriber(999)
        self.assertFalse(result)


class NewsLetterManagerTest(TestCase):

    def setUp(self):
        self.newsletter_data = {
            'subject': 'Weekly Update',
            'html_content': '<h1>Content</h1>',
            'send_time': None
        }
        self.newsletter = NewsLetterManager.store_newsletter(**self.newsletter_data)

    def test_store_newsletter(self):
        self.assertIsNotNone(self.newsletter)
        self.assertEqual(self.newsletter.subject, self.newsletter_data['subject'])

    def test_get_newsletter_by_id(self):
        retrieved_newsletter = NewsLetterManager.get_newsletter_by_id(self.newsletter.id)
        self.assertEqual(retrieved_newsletter, self.newsletter)

    def test_update_newsletter(self):
        new_data = {'subject': 'Monthly Update'}
        result = NewsLetterManager.update_newsletter(self.newsletter.id, **new_data)
        self.assertTrue(result)
        self.newsletter.refresh_from_db()
        self.assertEqual(self.newsletter.subject, 'Monthly Update')

    def test_update_non_existent_newsletter(self):
        result = NewsLetterManager.update_newsletter(999, subject='New Subject')
        self.assertFalse(result)

    def test_delete_newsletter(self):
        result = NewsLetterManager.delete_newsletter(self.newsletter.id)
        self.assertTrue(result)
        self.assertIsNone(NewsLetterManager.get_newsletter_by_id(self.newsletter.id))

    def test_delete_non_existent_newsletter(self):
        result = NewsLetterManager.delete_newsletter(999)
        self.assertFalse(result)


class NewsLetterOpenManagerTest(TestCase):

    def setUp(self):
        # Create a subscriber and a newsletter for testing
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

    def test_store_newsletter_open(self):
        # Store a newsletter open event with opened set to False initially
        newsletter_open = NewsLetterOpenManager.store_newsletter_open(
            track_id=uuid.uuid4(),
            subscriber=self.subscriber,
            newsletter=self.newsletter,
            opened=False,  # Initially set to False
            opened_at=None  # No timestamp yet
        )
        self.assertIsNotNone(newsletter_open)
        self.assertEqual(newsletter_open.subscriber, self.subscriber)
        self.assertEqual(newsletter_open.newsletter, self.newsletter)
        self.assertFalse(newsletter_open.opened)  # Check that opened is False
        self.assertIsNotNone(newsletter_open.track_id)  # Ensure track_id is generated

    def test_get_newsletter_open_by_track_id(self):
        # Store a newsletter open event
        newsletter_open = NewsLetterOpenManager.store_newsletter_open(
            track_id=uuid.uuid4(),
            subscriber=self.subscriber,
            newsletter=self.newsletter,
            opened=False,
            opened_at=None
        )

        # Retrieve the newsletter open event by track_id
        retrieved_newsletter_open = NewsLetterOpenManager.get_newsletter_open_by_track_id(newsletter_open.track_id)
        self.assertEqual(retrieved_newsletter_open, newsletter_open)

    def test_get_newsletter_open_by_non_existent_track_id(self):
        # Attempt to retrieve a newsletter open event with a non-existent track_id
        retrieved_newsletter_open = NewsLetterOpenManager.get_newsletter_open_by_track_id(uuid.uuid4())
        self.assertIsNone(retrieved_newsletter_open)

    def test_update_newsletter_open_by_id(self):
        # Store a newsletter open event
        newsletter_open = NewsLetterOpenManager.store_newsletter_open(
            track_id=uuid.uuid4(),
            subscriber=self.subscriber,
            newsletter=self.newsletter,
            opened=False,
            opened_at=None
        )

        # Update the newsletter open record by ID
        updated = NewsLetterOpenManager.update_newsletter_open_by_id(
            newsletter_open.id,
            opened=True,  # Change opened to True
            opened_at=timezone.now()
        )
        self.assertTrue(updated)

        # Retrieve the updated record and check the values
        updated_newsletter_open = NewsletterOpen.objects.get(id=newsletter_open.id)
        self.assertTrue(updated_newsletter_open.opened)

    def test_update_non_existent_newsletter_open_by_id(self):
        # Attempt to update a non-existent newsletter open record
        updated = NewsLetterOpenManager.update_newsletter_open_by_id(999, opened=False)
        self.assertFalse(updated)

    def test_update_newsletter_open_by_track_id(self):
        # Store a newsletter open event
        newsletter_open = NewsLetterOpenManager.store_newsletter_open(
            track_id=uuid.uuid4(),
            subscriber=self.subscriber,
            newsletter=self.newsletter,
            opened=False,
            opened_at=None
        )

        # Update the newsletter open record by track_id
        updated = NewsLetterOpenManager.update_newsletter_open_by_track_id(
            newsletter_open.track_id,
            opened=True,  # Change opened to True
            opened_at=timezone.now()
        )
        self.assertTrue(updated)

        # Retrieve the updated record and check the values
        updated_newsletter_open = NewsletterOpen.objects.get(track_id=newsletter_open.track_id)
        self.assertTrue(updated_newsletter_open.opened)

    def test_update_non_existent_newsletter_open_by_track_id(self):
        # Attempt to update a non-existent newsletter open record by track_id
        updated = NewsLetterOpenManager.update_newsletter_open_by_track_id(uuid.uuid4(), opened=False)
        self.assertFalse(updated)
