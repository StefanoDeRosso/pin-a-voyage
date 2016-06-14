from .models import CustomUser
from django.contrib.auth import get_user_model


class CustomUserAuth(object):
     def authenticate(self, username=None, password=None):
         user_cls = get_user_model()
         try:
             user = user_cls.objects.get(email=username)
             if user.check_password(password):
                 return user
         except user_cls.DoesNotExist:
             return None
         except:
             return None

     def get_user(self, user_id):
         user_cls = get_user_model()
         try:
             return user_cls.objects.get(pk=user_id)
         except user_cls.DoesNotExist:
             return None

'''
class CustomUserAuth(object):
	
	def authenticate(self, username=None, password=None):
		try:
			user = CustomUser.objects.get(email=username)
			if user.check_password(password):
				return user
		except CustomUser.DoesNotExist:
			return None
				
	def get_user(self, user_id):
		try:
			user = CustomUser.objects.get(pk=user_id)
			if user.is_active:
				return user
			return None
		except CustomUser.DoesNotExist:
			return None
'''
