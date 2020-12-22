import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request,'pages/home.html', context={}, status=400)

# saves form to DB after POST request
# handles redirect/render
def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None) # TweetForm class initialized with optional data
    next_url = request.POST.get('next') or None
    print('Request url: ', request.get_full_path())
    # print('Next url: ' + next_url)
    # If the form has valud content (aka there's likely been a POST request)
    # save it to the model
    if form.is_valid():
        obj = form.save(commit=False) # save returns a model object that hasn't been saved to the DB yet
        # do other form related logic in between
        obj.save() # save the object to the database
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 is for created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context={"form" : form})

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consumed by Javascript/UI Framework
    returns json data
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
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