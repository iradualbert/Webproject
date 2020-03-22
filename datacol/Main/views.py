from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import ListView
from .models import Post
from django.urls import reverse

# Create your views here.

def home(request):
    posts = Post.objects.all()
    context = {
        'datas' : posts
    }
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html')