import random
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Tweet

def home_view(request, *args, **kwargs):
    return render(request,'pages/home.html', context={}, status=400)

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consumed by Javascript/UI Framework
    returns json data
    """
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content, "likes" : random.randint(0, 123)} for x in qs]
    data = {
        "isUser": False,
        'response': tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consumed by Javascript/UI Framework
    returns json data
    """

    print(args, kwargs)
    
    data = {
        'id' : tweet_id,
        # 'image_path' = obj.image,
    }
    status = 200
    try:
        obj= Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404

    return JsonResponse(data, status=status)