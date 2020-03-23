import secrets
from django.shortcuts import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse,HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Channel, Topic, ProductService, Subscriber, Question
from .forms import CreateChannel, CreateChannelTopic, CreateQuestion, CreateAnswer
from .lazy_loading import lazy_loading_forms

class ProductDetailView(DetailView):
    model = ProductService

class ChannelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Channel
    fields = ['channel_name', 'channel_username', 'channel_profile_pic', 'bio', 'website',
              'privacy', 'category']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        channel = self.get_object()
        if self.request.user == channel.owner:
            return True
        return False

class TopicCreateView\
            (LoginRequiredMixin, CreateView):
    model = Topic
    fields = ['topic_title', 'description', 'topic_image']

    def form_valid(self, form):
        form.instance.parent_channel = self.get_object()
        return super().form_valid(form)

class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateQuestion
    template_name = 'channel/create_question.html'
    redirect_field_name = 'home_page'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return lazy_loading_forms(request, self.form_class, form_type='create_question')
        channel_info = get_object_or_404(Channel, channel_code=self.kwargs['channel_code'])
        form = self.form_class()
        form.fields["question_topic"].queryset = Topic.objects.filter(parent_channel=channel_info)
        if channel_info:
            return render(request, self.template_name, {'form':form, 'title': 'Add Question'})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_info = self.request.user
        self.object.channel_info = get_object_or_404(Channel, channel_code=self.kwargs['channel_code'])
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Question Saved Successfully!")
        return reverse('home_page')

class AnswerCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateAnswer
    template_name = 'channel/answer_form.html'
    
    def get(self, request, *args, **kwargs):
        current_user = self.request.user
        channel_info = get_object_or_404(Channel, channel_code=self.kwargs['channel_code'])

        if channel_info.private:
            if channel_info.is_admin(current_user) or channel_info.owner == current_user:
                question_info = get_object_or_404(Question, pk=self.kwargs['pk'])
                form = self.form_class()
                if channel_info:
                    return render(request, self.template_name,
                                  {'form': form, 'title': 'Add Answer', 'question': question_info})
            else:
                return HttpResponseForbidden()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_info = self.request.user
        self.object.channel_info = get_object_or_404(Channel, channel_code=self.kwargs['channel_code'])
        self.object.question_info= get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Question Saved Successfully!")
        return reverse('home_page')



@login_required
def create_channel(request):
    try:
        channel = Channel.objects.get(owner=request.user)
        channel_code = channel.channel_code
        return redirect('channel-detail', channel_code=channel_code)
    except:
        if request.method == 'POST':
            form = CreateChannel(request.POST)
            if form.is_valid():
                channel_code = secrets.token_hex(8)
                ## Make sure the channel with the same channel_code does not exist
                channel = Channel.objects.filter(channel_code=channel_code)
                if channel:
                    while True:
                        channel_code = secrets.token_hex(8)
                        channel = Channel.objects.filter(channel_code=channel_code)
                        if channel:
                            pass
                        else:
                            break
                user = request.user
                channel_name = form.cleaned_data['channel_name']
                channel_username = form.cleaned_data['channel_username']
                website = form.cleaned_data['website']
                bio = form.cleaned_data['description']
                new_channel = Channel(owner=user,
                                      channel_name=channel_name,
                                      channel_code=channel_code,
                                      channel_username=channel_username,
                                      website=website,
                                      bio=bio,)
                new_channel.save()
                messages.success(request, f'Channel Created Successfully!')
                return redirect('channel-detail', channel_code=channel_code)
        else:
           form = CreateChannel()
        return render(request, 'channel/channel_form.html', {'form': form, 'title': 'Create A Channel'})

@login_required
def create_channel_topic(request, channel_code):
    current_user = request.user
    channel = get_object_or_404(Channel, channel_code=channel_code)
    if channel.owner == current_user:
        if request.method == 'POST':
            form = CreateChannelTopic(request.POST)
            if form.is_valid():
                topic_title = form.cleaned_data['title_name']
                website = form.cleaned_data['link']
                description = form.cleaned_data['description']
                new_topic = Topic(topic_title=topic_title,
                                  website=website,
                                  parent_channel=channel,
                              )
                if description:
                    new_topic.description = description
                new_topic.save()
                if request.is_ajax():
                    return JsonResponse({"status": "ok"})
                else:
                    messages.success(request, 'Created')
                    return redirect('channel-detail', channel_code=channel_code)
        else:
            form = CreateChannelTopic()
    else:
        return HttpResponseForbidden()
    return render(request, 'channel/topic_form.html', {'form':form, 'title': f'{channel.channel_name} - New'})


def channel_home(request, channel_code):
    channel = get_object_or_404(Channel, channel_code=channel_code)
    user = request.user
    if user.is_authenticated:
        sub_status = channel.is_subscribed(request)
        if sub_status:
            sub_button = 'Subscribed'
        else:
            sub_button = 'Subscribe'
    else:
        sub_button = 'Subscribe'
    t_form = CreateChannelTopic()
    return render(request, 'channel/channel_detail.html', {'title': channel.channel_username, 'object': channel, 't_form': t_form, 'sub_button_text': sub_button})

def channel_subscribe(request, channel_code):
    user = request.user
    if request.is_ajax() and user.is_authenticated:
        channel = Channel.objects.get(channel_code=channel_code)
        if channel.owner == user:
            return JsonResponse({"response": "invalid request", "status": "ok"})
        subscriber = Subscriber.objects.filter(channel_id=channel.id, user_id=user.id)
        if subscriber:
            subscriber.delete()
            return JsonResponse({"response": "Unsubscribed", "status": "ok"})
        else:
            channel.add_subscriber(user_id=user.id)
            return JsonResponse({"response": "Subscribed", "status": "ok"})
    else:
        return HttpResponseNotAllowed('405')


def create_question(request, channel_code):
    channel = get_object_or_404(Channel, channel_code=channel_code)
    user = request.user


def channel_add_admin(request, channel_code):
    channel = get_object_or_404(Channel, channel_code=channel_code)
    try:
        user = User.objects.get(username=request.POST['username'])
    except:
        return JsonResponse({'success': False, 'status': 'not_found'})

    current_user = request.user
    if (current_user != channel.owner):
        return JsonResponse({'success': False, 'status': 'Invalid'})

    if channel.is_admin(user):
        channel.remove_admin(user)
        return JsonResponse({'success': True, 'status': 'removed'})

    else:
        channel.add_admin(user)
        return JsonResponse({'success': True, 'status': 'ok'})

