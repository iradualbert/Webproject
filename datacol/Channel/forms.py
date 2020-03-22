from django import forms
from .models import Channel, Topic, Question, Answer

class CreateChannel(forms.Form):


    channel_name = forms.CharField(required=True, max_length=50,
                                   label='',
                                   widget=forms.TextInput(attrs={'placeholder': 'Channel Name...'}))
    channel_username = forms.CharField(required=True, max_length=30,
                                       label='',
                                       widget=forms.TextInput(attrs={'placeholder': '@'}))
    description = forms.CharField(required=False,
                                  label='',
                                  widget=forms.Textarea(attrs={'placeholder': 'Short description', 'rows': 4}),
                                  max_length=500)
    website = forms.CharField(required=False, max_length=500,
                              label='Website (Optional)',
                              widget=forms.TextInput(attrs={'placeholder': 'www.example.com'}))
    public = forms.BooleanField(required=False, label='By creating Channel, I agree to the terms and conditions')

    def clean(self):
        username = self.cleaned_data.get('channel_username')
        from .models import Channel
        channel = Channel.objects.filter(channel_username=username)
        if channel:
            raise forms.ValidationError('This Username is taken!')


class CreateChannelTopic(forms.Form):
    title_name = forms.CharField(required=True, max_length=50, help_text='', label='',
                                 widget=forms.TextInput(attrs={'placeholder': 'Name..', 'autofocus': True}))
    link = forms.CharField(required=False, max_length=100,
                           label='',
                           widget=forms.TextInput(attrs={'placeholder': 'Website or link...', 'autofocus': True}))
    description = forms.CharField(required=False, max_length=500,
                                  label='',
                                  widget=forms.Textarea(attrs={'placeholder': 'Write a short description.....', 'id': 'textarea', 'rows': 4, 'autofocus': True}))

    def clean(self):
        # Make sure the topic name does not exist already.
        pass
class CreateQuestion(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_title', 'question_detail', 'question_topic']
        widgets = {
            'question_detail': forms.Textarea(attrs={'placeholder': 'Optional: Question detail......', 'rows': 4}),
            'question_title': forms.TextInput(
                attrs={'placeholder': 'Write your question here...', 'rows': 4}),
            'question_topic': forms.Select(
                attrs={'placeholder': 'Write your question here...', 'rows': 4}),
        }

        labels = {
            'question_title': '',
            'question_detail': '',
            'question_topic': 'Choose a topic to more specific(Optional)'
        }


class CreateAnswer(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_content', 'answer_link']
        labels = {
            'answer_content': '',
            'answer_link': 'Include a link for more details(Optional)',
        }
        widgets = {
            'answer_content': forms.Textarea(
                attrs={'placeholder': 'Type the answer here......', 'rows': 5}),

            'answer_link': forms.TextInput(
                attrs={'placeholder': 'https://www.example.com', 'rows': 5,
                       }),
        }