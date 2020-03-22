from django.contrib import admin
from .models import Profile,History, SavedList, FlashCard, Notification
# Register your models here.

admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(SavedList)
admin.site.register(FlashCard)
admin.site.register(History)
