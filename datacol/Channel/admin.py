from django.contrib import admin
from .models import Channel, Topic, ProductService, Question, Answer, RateReview, TopicRateReview, Subscriber, ChannelAdmin
from image_cropping import ImageCroppingMixin


# Register your models here.

'''class ChannelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    search_fields = ['channel_name', 'channel_username']
    list_display = ['channel_name', 'owner', 'channel_username', 'channel_code']'''

admin.site.register(Channel)
admin.site.register(Topic)
admin.site.register(ProductService)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(RateReview)
admin.site.register(TopicRateReview)
admin.site.register(Subscriber)
admin.site.register(ChannelAdmin)
