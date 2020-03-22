from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Error, Reported, Post
# Register your models here.
class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Error)
admin.site.register(Reported)
admin.site.register(Post, PostAdmin)
