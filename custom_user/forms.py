from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from collections import OrderedDict
from django import forms
from parsley.decorators import parsleyfy
from stdimage.models import StdImageField

from models import CustomUser, CustomUserManager


@parsleyfy
class CustomUserCreationForm(UserCreationForm):
	"""
	A form that creates a user, with no privileges, from the given email and password.
	"""
	email = forms.CharField(label='', required=True, widget = forms.TextInput(
        attrs = {
            'placeholder': 'E-mail',
			'class': 'form-control',
			'id': 'email',
			'data-parsley-remote': '',
			'data-parsley-remote-options': '{ "type": "POST", "dataType": "json" }',
			'data-parsley-remote': '/check_email/',
			'parsley-remote-method': 'POST',
			'data-parsley-remote-validator': 'emailCheck',
			'data-parsley-remote-message': 'The E-mail is already used.'
        }
    ))
    
	first_name = forms.CharField(label='', required=True, widget = forms.TextInput(
        attrs = {
            'placeholder': 'First name',
			'class': 'form-control'
        }
    ))
    
	second_name = forms.CharField(label='', required=True, widget = forms.TextInput(
        attrs = {
            'placeholder': 'Last name',
			'class': 'form-control'
        }
    ))
    
	password1 = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs = {
            'placeholder': 'Password',
			'class': 'form-control',
			'id': 'password1'
        }))
        
	password2 = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs = {
            'data-parsley-equalto': '#password1',
            'placeholder': 'Password confirmation (enter the same password as above, for verification)',
			'class': 'form-control'
        }))
		
	class Meta:
		model = CustomUser
		fields = ("email", "first_name", "second_name", "password1", "password2")
	
	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			CustomUser._default_manager.get(email=email)
		except CustomUser.DoesNotExist:
			return email
		raise forms.ValidationError('Duplicate e-mail')
		
	def save(self, commit=True):
		user = super(CustomUserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password2'])
		if commit:
			user.is_active = False
			user.save()
		return user

class SignupForm(forms.Form):
	first_name = forms.CharField(max_length=30, label='First name')
	second_name = forms.CharField(max_length=30, label='Last name')

	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.second_name = self.cleaned_data['second_name']
		user.save()


@parsleyfy
class CustomLoginForm(forms.ModelForm):
	"""
	A form that login a user.
	"""
	
	email = forms.EmailField(label='', required=True, widget = forms.TextInput(
        attrs = {
            'placeholder': 'E-Mail',
			'class': 'form-control',
			'id': 'login-email'
        }
    ))
    
	password1 = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs = {
            'placeholder': 'Password',
			'class': 'form-control',
			'id': 'login-password',
			'data-parsley-trigger': 'focusout'
        }))
        
	class Meta:
		model = CustomUser
		fields = ('email',)
    
    

class CustomUserChangeForm(forms.ModelForm):
	email = forms.EmailField(label='', required=True, widget = forms.TextInput(
		attrs = {
			'placeholder': 'E-Mail',
			'class': 'form-control'
		}
	))
    
	first_name = forms.CharField(label='', required=True, widget=forms.TextInput(
		attrs = {
			'placeholder': 'First name',
			'class': 'form-control'
		}
	))
        
	second_name = forms.CharField(label='', required=True, widget=forms.TextInput(
		attrs = {
			'placeholder': 'Second name',
			'class': 'form-control'
		}
	))
	
	avatar = forms.ImageField(label='', required=False, widget=forms.FileInput(
		attrs = {
			'placeholder': 'Profile pic',
			'class': 'form-control',
			'id': 'avatar_url',
			'name': 'avatar_url'
		}
	))

	class Meta:
		model = CustomUser
		fields = ('email', 'first_name', 'second_name', '_avatar')

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(CustomUserChangeForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].required = False

	def clean_email_address(self):
		email = self.cleaned_data.get('email')
		if self.user and self.user.email == email:
			return email
		if CustomUser.objects.filter(email=email).count():
			raise forms.ValidationError(u'That email address already exists.')
		return email

	def save(self, commit=True):
		user = super(CustomUserChangeForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		
		if commit:
			user.save()
			
		return user
		
class PasswordChangeForm(SetPasswordForm):
    
	new_password1 = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs = {
			'placeholder': 'New password',
			'class': 'form-control',
			'id': 'login-password',
			'data-parsley-trigger': 'focusout'
        }))
       
	new_password2 = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs = {
			'placeholder': 'Re-write new password',
			'class': 'form-control',
			'id': 'login-password',
			'data-parsley-trigger': 'focusout'
        }))
        
	class Meta:
		model = CustomUser
		fields = ('old_password', 'new_password1', 'new_password2')
		
	"""
	A form that lets a user change their password by entering their old
	password.
	"""
	error_messages = dict(SetPasswordForm.error_messages, **{
		'password_incorrect': _("Your old password was entered incorrectly. "
								"Please enter it again."),
	})
	old_password = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs = {
			'placeholder': 'Old password',
			'class': 'form-control',
			'id': 'login-password',
			'data-parsley-trigger': 'focusout'
        }))

	def clean_old_password(self):
		"""
		Validates that the old_password field is correct.
		"""
		old_password = self.cleaned_data["old_password"]
		if not self.user.check_password(old_password):
			raise forms.ValidationError(
				self.error_messages['password_incorrect'],
				code='password_incorrect',
			)
		return old_password


PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)

'''
class CustomUserChangeForm(UserChangeForm):
	"""
	A form for updating users. Includes all the fields on the user, but replaces the password field with admin's password hash display field.
	"""
	
	def __init__(self, *args, **kwargs):
		super(CustomUserChangeForm, self).__init__(*args, **kwargs)
		
	class Meta:
		model = CustomUser
		fields = ("email", "first_name", "second_name",)
'''
