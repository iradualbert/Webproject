from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponseNotAllowed, HttpResponse

from .models import Channel

def lazy_loading_topics(request, channel_code):
    if True:
        channel = get_object_or_404(Channel, channel_code=channel_code)
        topics = channel.get_channel_topics()

        # HTML topics list
        topics_html = loader.render_to_string(
            'Channel/topics.html',
            {'topics': topics,
             'title': f'{channel.channel_name} Topics',
             'is_ajax': False,
             }
        )
        output_data = {
            'topics_html': topics_html,
        }
        return HttpResponse(topics_html)
    else:
        return HttpResponseNotAllowed('405')

def lazy_loading_forms(request, form, form_type=None):
    if form_type is None:
        form_type = request.GET('form-name')
    try:
        form_html = loader.render_to_string(
            f"channel/{form_type}.html",
            {'is_ajax': request.is_ajax(),
             'csrf_token': request.COOKIES['csrftoken'],
             'form': form}
        )
        output_data = {'form_html': form_html}
        return HttpResponse(form_html)

    except:
        return JsonResponse({'success': False, 'status': 'not found'})

