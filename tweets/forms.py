from django import forms

from .models import Tweet


MAX_TWEET_LENGTH = 240

# TweetForm is a subclass of a model, hence a model itself
# NOTE: ModelForm maps a model class's fields to HTML form
class TweetForm(forms.ModelForm):
    # provide metadata
    class Meta: 
        model = Tweet
        fields = ['content']
    
    # This method does any cleaning that is specific to that particular 
    # fieldname/attribute (clean_<fieldname>() naming convention)
    # So here, checking a max length counts as "cleaning"
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long.")
        return content

    