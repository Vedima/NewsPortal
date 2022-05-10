from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import Post, Author, PostCategory
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['header', 'text', 'post_cat']
        #labels = {'author': 'Автор', }

#class NewsForm(forms.ModelForm):
 #   class Meta:
  #      model = Post
   #     fields = ['author', 'header', 'text', 'post_cat']
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['username', 'first_name', 'last_name', 'password', ]

class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

class SubscribeForm(forms.ModelForm):
    class Meta:
        #model = Post
        model = PostCategory
        fields = ['category']