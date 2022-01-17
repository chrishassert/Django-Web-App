from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import *
from django.core.files.storage import FileSystemStorage
from datetime import timezone, timedelta


# Create your models here.

# obtained from 'https://stackoverflow.com/questions/6350153/getting-username-in-imagefield-upload-to-path'
def upload_to(instance, filename):
    return '%s/%s' % (instance.user.username, filename)

def book_upload(instance, filename):
    print("Instance")
    print( instance)
    return 'texbook/%s/%s' % (instance.userid.user, filename)

# this creates a profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    profileImage = models.ImageField(upload_to=upload_to, null=True, blank=True, default='default_image.jpg')
    # this function creates a profile when a user logs in (maybe, haven't tested it)
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()



# The Listing model creates a textbook listing
class Listing(models.Model):
    seller_name = models.CharField(max_length=10)
    book_image = models.ImageField(upload_to=book_upload, null=True, blank=True, default='default_image.jpg')
    book_title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20)
    book_course = models.CharField(max_length=30)
    book_description = models.CharField(max_length=500, default="No description available. Message seller for more details.")
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text='Please enter a price')
    userid = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.book_title

class Message(models.Model):

    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="recipient", on_delete=models.CASCADE) # almost same as above field, just change the related-name
    message = models.TextField()# text field
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now
    def inbox(self, Message, request):
        Message.objects.filter(sender=request.user)
    def sent_messages(self, Message, request):
        Message.objects.filter(sender=request.user)

class Map(models.Model):

    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    send = models.ForeignKey(User, related_name="send", on_delete=models.CASCADE) # almost same as above field, just change the related-name
    pub_date = models.DateTimeField('date published')

    def get_user(self):
        return self.user
    def get_send(self):
        return self.send
    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now
    def inbox(self, Message, request):
        Message.objects.filter(sender=request.user)
    def sent_messages(self, Message, request):
        Message.objects.filter(sender=request.user)

class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    group_name = models.CharField(max_length=512, default="group",blank=False,null=False)