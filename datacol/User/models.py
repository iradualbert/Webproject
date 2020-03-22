from threading import Thread
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    languages = (
        ('en', 'English'),
        ('fr', 'French'),
        ('tr', 'Turkish'),
        ('kiny', 'Kinyarwanda')
    )
    language = models.CharField(max_length=20, default='English', choices=languages)
    genders = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unmentioned', 'Unmentioned'),
    )
    careers_and_occupations = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Unmentioned', 'Unmentioned'),
    )
    gender = models.CharField(max_length=15,default='Unmentioned', choices=genders, null=True)
    phone_number = PhoneNumberField(null=True)
    birthday = models.DateField(null=True)
    date_created = models.DateTimeField(default=datetime.utcnow)
    career = models.CharField(default='Unmentioned', max_length=100, choices=careers_and_occupations)
    profile_pic = models.ImageField(default='media/profile_pics/Noprofile.PNG', upload_to='media/profile_pics')
    Channel_owner = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    country = CountryField(blank_label='Select Country')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)



class SavedList(models.Model):
    total = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=30, unique=True)
    language = models.CharField(max_length=10, default='English')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    privacy_status =(
        ('Private', 'Private'),
        ('Public', 'Public'),
    )
    privacy = models.CharField(default='Private', choices=privacy_status, null=False, max_length=8)
    date_created = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f'{self.name}---{self.date_created}'

    class Meta:
        ordering =['date_created']

class FlashCard(models.Model):
    language = models.CharField(max_length=10, default='English')
    name = models.CharField(max_length=30, unique=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    privacy_status = (
        ('Private', 'Private'),
        ('Public', 'Public'),
    )
    privacy = models.CharField(default='Private', choices=privacy_status, null=False, max_length=8)
    date_created = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f'{self.name}---{self.date_created}'

    class Meta:
        ordering = ['date_created']
class History(models.Model):

    user_info = models.ForeignKey(User, on_delete=models.CASCADE)
'''Testing 
   Resizing and croping pictures
'''
class Photo(models.Model):
    file = models.ImageField()
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

class Notification(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    url = models.URLField(null=False)
    time_sent = models.DateTimeField(default=datetime.utcnow)
    seen = models.BooleanField(default=False, null=False)

    def send_notification(to, description, url):
        new_notification = Notification(to=to, description=description, url=url)
        new_notification.save()
        return new_notification

    def get_notification(self, user):
        notifications = Notification.objects.filter(to=user)
        return notifications

    def delete_notification(self):
        notific = Notification.objects.get(pk=self.pk)
        notific.delete()
        return notific
