import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL # reference to built in django user model, provides many common attributes

class Tweet(models.Model):
    # Maps to SQL Data
    # id = models.AutoField(primary_key=True)

    # FK -> many users can have many tweets
    # CASCADE option means on owner user delete, delete all tweets
    # using null=True, a model field can be optionally empty
    user = models.ForeignKey(User, on_delete=models.CASCADE)     
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    class Meta:
        ordering = ['-id'] # newest tweet should be first in this case

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }