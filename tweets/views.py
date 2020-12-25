import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .forms import TweetForm
from .models import Tweet
from .serializers import TweetCreateSerializer, TweetSerializer, TweetActionSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    print(request.user or None)
    return render(request,'pages/home.html', context={}, status=400)

# saves form to DB after POST request
# handles redirect/render
def tweet_create_view_pure_django(request, *args, **kwargs):
    """
    REST API Create View -> DRF
    """

    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401) # 401 means not authorized
        return redirect(settings.LOGIN_URL)

    form = TweetForm(request.POST or None) # TweetForm class initialized with optional data
    next_url = request.POST.get('next') or None
    print('Request url: ', request.get_full_path())
    # print('Next url: ' + next_url)
    # If the form has valud content (aka there's likely been a POST request)
    # save it to the model
    if form.is_valid():
        obj = form.save(commit=False) # save returns a model object that hasn't been saved to the DB yet
        # do other form related logic in between
        obj.user = request.user
        obj.save() # save the object to the database
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 is for created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    # if form has errors
    if form.errors:
        return JsonResponse(form.errors, status=400) # 400 is for errors
    return render(request, 'components/form.html', context={"form" : form})


@api_view(['POST']) # http method from client == POST
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated]) # if user is authenticated, then they have access to this view
def tweet_create_view(request, *args, **kwargs):
    """
    REST API Create View -> DRF
    """
    serializer = TweetCreateSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True): # raise exception sends correct error back implictly
         serializer.save(user=request.user)
         return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['POST']) # http method from client == POST
@permission_classes([IsAuthenticated]) # if user is authenticated, then they have access to this view
def tweet_action_view(request, *args, **kwargs):
    """
    id is required
    Action options are: like, unlike, retweet
    These Actions are what all users have control over regarding a tweet
    """
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        
        # deserialize
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')
        
        # find tweet in DB 
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        
        if action == 'like':
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'retweet':
            new_tweet = Tweet.objects.create(
                user=request.user, 
                parent=obj,
                content=content,
            )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=200)
    return Response({'message': f'Tweet {action}ed.'}, status=201)

@api_view(['GET']) # only http method allowed == GET
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API Detail View -> DRF
    returns details for tweet with id=tweet_id as json
    """
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj) # qs is multiple instances, and many is explicit flag for that
    return Response(serializer.data)

@api_view(['DELETE', 'POST']) 
@permission_classes([IsAuthenticated]) # if user is authenticated, then they have access to this view
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    """
    REST API Delete View -> DRF
    """
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists(): # if no tweet exists after user filteration
        return Response({'message': 'You cannot delete this tweet.'}, status=404)
    obj = qs.first()
    obj.delete()
    return Response({'message': 'Tweet removed.'}, status=200)

@api_view(['GET']) # only http method allowed == GET
def tweet_list_view(request, *args, **kwargs):
    """
    REST API List View -> DRF
    returns all tweets as json response
    """
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True) # qs is multiple instances, and many is explicit flag for that
    return Response(serializer.data)


def tweet_list_view_pure_django(request, *args, **kwargs):
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

def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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