from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import Post, Author

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'header', 'text', 'post_cat']
        #labels = {'author': 'Автор', }

#class NewsForm(forms.ModelForm):
 #   class Meta:
  #      model = Post
   #     fields = ['author', 'header', 'text', 'post_cat']