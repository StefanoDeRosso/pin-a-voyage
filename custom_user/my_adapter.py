from django.contrib.auth.models import User

from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import CustomUser
from custom_user.backends import CustomUserAuth
from django.contrib.auth import login


class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        user = sociallogin.user
        if user.id:  
            return
        try:
            user = User.objects.get(email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'                
            login(request, user)
        except User.DoesNotExist:
            pass

