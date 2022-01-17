from django.test import TestCase, RequestFactory
from main.models import *
from django.core.exceptions import *
from django.contrib.auth.models import AnonymousUser, User
from django.test.client import Client

# Create your tests here.

class ListingTestCase(TestCase):
    def setUp(self):
        testListing = Listing(book_title='test',author='James',isbn='2503',book_course='CS3240',price='50')
        testListing.save()
    def test_create_listing(self): # Tests to make sure Listings fields are correct when created
        a = Listing.objects.get(book_title='test')
        self.assertEqual(a.book_title, 'test')
        self.assertEqual(a.author, 'James')
        self.assertEqual(a.isbn,'2503')
        self.assertEqual(a.book_course, 'CS3240')
        self.assertEqual(a.price, 50.00)
    def test_invalid_input(self): # This tests to make sure that a ValidationError exception is thrown when price is a non-decimal number
        a = Listing.objects.get(book_title='test')
        with self.assertRaises(ValidationError):
            a.price = 'a'
            a.save()

class ProfileTestCase(TestCase):
    def setUp(self):
        user = User(username='test')
        testProfile = Profile(user=user)
    
class PhoneNumberUpdateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser("testing", "testing@gmail.com", "password")
        a = Profile.objects.filter(user=self.user).update(phone_number="1234567890")

    def test_phone_number_update(self):
        request = self.factory.get('/customer/details')
        request.user = self.user
        a = Profile.objects.get(user=request.user)
        self.assertEqual(a.phone_number, "1234567890")

class MessageTestCase(TestCase):
    def setUp(self):
        sender = User.objects.create(username='ljc2sh')
        recipient = User.objects.create(username='jw8kc')

    def test_create_message(self): # Tests to make sure Listings fields are correct when created
        larry = User.objects.all().filter(username='ljc2sh')
        sender = larry.first()
        jammie = User.objects.all().filter(username='jw8kc')
        recipient = jammie.first()
        message = Message(sender=sender, recipient=recipient, message='hey', pub_date='1990-12-30T23:59:30Z')
        message.save()
        sender = Message.objects.all()
        m = sender.first()
        self.assertEqual(m.sender.username, 'ljc2sh')
        self.assertEqual(m.recipient.username, 'jw8kc')
        self.assertEqual(m.message,'hey')
        self.assertEqual(str(m.pub_date), '1990-12-30 23:59:30+00:00')

    def test_empty_message(self):  # Tests to make sure Listings fields are correct when created
        larry = User.objects.all().filter(username='ljc2sh')
        sender = larry.first()
        jammie = User.objects.all().filter(username='jw8kc')
        recipient = jammie.first()
        message = Message(sender=sender, recipient=recipient, message='', pub_date='1990-12-30T23:59:30Z')
        message.save()
        sender = Message.objects.all()
        m = sender.first()
        self.assertEqual(m.sender.username, 'ljc2sh')
        self.assertEqual(m.recipient.username, 'jw8kc')
        self.assertEqual(m.message, '')
        self.assertEqual(str(m.pub_date), '1990-12-30 23:59:30+00:00')

class MapTestCase(TestCase):
    def setUp(self):
        sender = User.objects.create(username='ljc2sh')
        recipient = User.objects.create(username='jw8kc')
        mmap = Map(user=sender, send=recipient, pub_date='1990-12-30T23:59:30Z')
        mmap.save()

    def test_create_map(self):  # Tests to make sure Listings fields are correct when created
        mess = Map.objects.all()
        mmap = mess.first()
        self.assertEqual(mmap.user.username, 'ljc2sh')
        self.assertEqual(mmap.send.username, 'jw8kc')
        self.assertEqual(str(mmap.pub_date), '1990-12-30 23:59:30+00:00')
