from django.db import models
from Channel.models import Channel, Topic
# Create your models here.

class Product(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    product_id = models.CharField(max_length=16, null=False, blank=False)
    guide = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}- {self.channel.channel_name}"

class UserGuide(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}-User guide"

class ProductQuestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    q_title = models.CharField(max_length=200, null=False, blank=False)
    detail = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}--{self.q_title}"

class ProductAnswer(models.Model):
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE)
    answer_content = models.TextField(null=False)
    date_time = models.DateTimeField(auto_now_add=True)

class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    p_image = models.ImageField(null=True, upload_to='media/product_pics')
    date_time = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(null=True)

