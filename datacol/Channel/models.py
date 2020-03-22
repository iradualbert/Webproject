from datetime import datetime
from django.db import models
from User.models import Notification
from django.contrib.auth.models import User
from django.urls import reverse
from image_cropping import ImageRatioField, ImageCropField

# Create your models here.
class Channel(models.Model):
    
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="channel_creator")
    channel_name = models.CharField(max_length=20)
    channel_username = models.CharField(max_length=20, unique=True, null=False)
    channel_code = models.CharField(max_length=20, unique=True)
    channel_profile_pic = ImageCropField(default='media/Noprofile.PNG', upload_to="media/channel_profile_pics")
    cropping = ImageRatioField('channel_profile_pic', '430x360')
    bio = models.TextField(max_length=200, null=True)
    website = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(default=datetime.utcnow)
    verified = models.BooleanField(default=False)
    private = models.BooleanField(default=True)
    category_choices = (
        ('Books', 'Books Publication'),
        ('Movies', 'Movies'),
        ('Education', 'Education'),
        ('Business', 'Business'),
        ('Personal', 'Personal Blog'),
        ('NGOS', 'Non Profit Organization'),
        ('Other', 'Other'),
    )
    category = models.CharField(max_length=50, choices=category_choices)
    #subscribers = models.ManyToManyField(User)
    search_fields = ('channel_name')

    def __str__(self):
        return f'{self.channel_name}- Owned by -{self.owner.email}'

    def get_absolute_url(self):
        return reverse('channel-detail', kwargs={'channel_code': self.channel_code})

    def get_subscribers_no(self):
        subscribers = Subscriber.objects.filter(channel_id=self.id)
        return subscribers.count()
    def get_subscribers(self):
        subscribers = Subscriber.objects.filter(channel_id=self.id)
        return subscribers
    def add_subscriber(self, user_id):
        new_sub = Subscriber(user_id=user_id, channel_id=self.id)
        new_sub.save()
        Notification.send_notification(to=self.owner,
                                       description="you have new subscriber to your channel",
                                       url=self.get_absolute_url())
        return new_sub
    def is_subscribed(self, request):
        sub = Subscriber.objects.filter(user_id=request.user.id, channel_id=self.id)
        if sub:
            return True
        else:
            return False
    def add_admin(self, user):
        new_admin = ChannelAdmin(user_info=user, channel_info=self)
        new_admin.save()
        return new_admin
    def get_admins(self):
        admins = ChannelAdmin.objects.filter(channel_info=self)
        return admins
    def remove_admin(self, user):
        admin = ChannelAdmin.objects.filter(channel_info=self, user_info=user)
        admin.delete()
        return admin

    """
    function to check if the current user is the admin of the channel_code
    """
    def is_admin(self, user):
        adm = ChannelAdmin.objects.filter(user_info=user, channel_info=self)
        if adm:
            return True
        else:
            return False

    def get_channel_topics(self):
        topics = Topic.objects.filter(parent_channel=self)
        return topics


class Subscriber(models.Model):
    user_id = models.IntegerField()
    channel_id= models.IntegerField()
    date_subscribed = models.DateTimeField(default=datetime.utcnow)
    notification = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}  user: {self.user_id}  channel: {self.channel_id}"

class ChannelAdmin(models.Model):
    user_info = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_info = models.ForeignKey(Channel, on_delete=models.CASCADE)
    role = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    notification = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} user: {self.user.id} - channel: {self.channel_info.channel_code} {self.channel_info.channel_name}"


class Topic(models.Model):
    topic_title = models.CharField(max_length=20)
    topic_image = models.ImageField(default='default_topic_pic', upload_to='media/topic_pics')
    description = models.TextField(null=True, blank=False)
    website = models.TextField(null=True, blank=False)
    parent_channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    subscribers = models.ManyToManyField(User, related_name="channel_subscribers")
    def __str__(self):
        return f'{self.topic_title}'

    def get_absolute_url(self):
        return reverse('topic-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['date_created']


class ProductService(models.Model):
    # TODO
    """
    - provide a step by step instructions about this product
    _ link or website for details
    _ Safety warning
    _ field based products or services 
    """

    product_name = models.CharField(max_length=50)
    product_profife_picture = models.ImageField(default='no_image', upload_to='Channel/product_profile_pics')
    guide_info = models.TextField(null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    business = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    product_info = models.TextField(null=True)
    date_created = models.DateTimeField(default=datetime.utcnow)
    admins = models.ManyToManyField(User, related_name='product_admin')
    class Meta:
        ordering = ['date_created']

class Question(models.Model):
    channel_info = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user_info = models.ForeignKey(User, on_delete=models.CASCADE, related_name="asked_by")
    question_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    question_title = models.CharField(max_length=250, null=False)
    question_detail = models.TextField(null=True, blank=True)  # short description to your question
    question_total_followers = models.IntegerField(default=0, null=True)
    question_followers = models.ManyToManyField(User, related_name="question_followers")
    question_total_answers = models.IntegerField(default=0, null=True)
    date_submitted = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        ordering = ['date_submitted']
    def __str__(self):
        return f"{self.question_title}--{self.channel_info.channel_name}"

    def get_question_answers(self):
        answers = Answer.objects.get(question_info=self)
        return answers
    def add_question_follower(self, user):
        new_follower = self.question_followers.add(user)
        return new_follower
    def add_answer(self, user, answer_content):
        answer = Answer(question_info=self, user_info=user, answer_content=answer_content)
        answer.save()
        return answer

class Answer(models.Model):
    question_info = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    user_info = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="answer_owner")
    answer_content = models.TextField(null=False)
    answer_link = models.CharField(null=True, max_length=1000, blank=True)
    answer_total_likes = models.IntegerField(default=0)
    answer_total_dislikes = models.IntegerField(default=0)
    answer_total_modifications = models.IntegerField(default=0)
    answer_total_rates = models.IntegerField(default=0)
    answer_average_rate = models.FloatField(null=True)
    answer_total_reviews = models.IntegerField(default=0)
    answer_total_shares = models.IntegerField(default=0)
    date_submitted = models.DateTimeField(auto_now_add=True)
    answer_total_views = models.IntegerField(default=0)
    answer_views = models.ManyToManyField(User)
    marks = models.FloatField(default=50)
    is_edited = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    class Meta:
        ordering = ['marks', 'date_submitted']


class AnswerView(models.Model):
    user_info = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    answer_info = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False)
    date_viewed= models.DateTimeField(auto_now_add=True)

# answering by images
class Photo(models.Model):
    # TODO
    # QUESTION

    caption = models.TextField(null=True)
    image = models.ImageField(null=False, upload_to='Channel/answer_pics')
# step by step answer


class StepByStep(models.Model):
    # TODO
    pass
class ByDrawing(models.Model):
    # TODO
    pass

class RateReview(models.Model):
    channel_info = models.ForeignKey(Channel, on_delete=models.CASCADE, null=False)
    user_info = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_submitted = models.DateTimeField(default=datetime.utcnow, null=False)
    review_content = models.TextField(null=False)
    rate = models.FloatField(null=False)

    class Meta:
        ordering = ['date_submitted']

class TopicRateReview(models.Model):
    channel_info = models.ForeignKey(Channel, on_delete=models.CASCADE, null=False)
    user_info = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_submitted = models.DateTimeField(default=datetime.utcnow, null=False)
    topic_review_content = models.TextField(null=False)
    topic_rate = models.FloatField(null=False)

    class Meta:
        ordering = ['date_submitted']

class ProductServiceRateReview(models.Model):
    product_info = models.ForeignKey(ProductService, on_delete=models.CASCADE, null=False)
    user_info = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_submitted = models.DateTimeField(default=datetime.utcnow, null=False)
    product_service_review_content = models.TextField(null=False)
    product_service_rate = models.FloatField(null=False)


    class Meta:
        ordering = ['date_submitted']
