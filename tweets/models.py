import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL # reference to built in django user model, provides many common attributes

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user who liked the tweet
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE) # Using quotes for "Tweet" because model is below and hasn't been declared yet
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    # Maps to SQL Data
    # id = models.AutoField(primary_key=True)

    # FK -> many users can have many tweets
    # CASCADE option means on owner user delete, delete all tweets
    # using null=True, a model field can be optionally empty
    user = models.ForeignKey(User, on_delete=models.CASCADE)     
    likes = models.ManyToManyField(User, related_name="tweet_user", blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id'] # newest tweet should be first in this case

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }