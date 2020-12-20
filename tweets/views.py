from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Tweet

def home_view(request, *args, **kwargs):
    print(args)
    print(kwargs)
    return HttpResponse("Hello Universe")

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    print(args)
    print(kwargs)
    try:
        obj= Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
    return HttpResponse(f'Hello {tweet_id} - {obj.content} Universe')