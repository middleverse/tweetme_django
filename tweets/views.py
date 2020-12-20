from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Tweet

def home_view(request, *args, **kwargs):
    print(args)
    print(kwargs)
    return HttpResponse("Hello Universe")

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by Javascript
    returns json data
    """

    print(args)
    print(kwargs)
    
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