from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils import timezone
from .models import Post, Comment, CustomUserManager, CustomUser
from forms import PostForm, CommentForm
from custom_user.forms import CustomUserCreationForm
from custom_user.backends import CustomUserAuth
from django.contrib.auth.decorators import login_required
# from django.core.context_processors import csrf
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login

def register(request):
	
	registered = False
	
	if request.method == 'POST':
		# user_form = CustomUserCreationForm(data=request.POST)
		user_form = CustomUserCreationForm(request.POST)
		
		if user_form.is_valid():
			user = user_form.save()
			
			user.set_password(user.password)
			user.save()
			
			registered = True
			
			return redirect('../')
			
		else:
			print user_form.errors
	else:
		user_form = CustomUserCreationForm()
			
	return render(request, 'register.html', {'user_form': user_form, 'registered': registered})

'''
def	login_custom(request):
	
	if request.method == 'POST':
		# login_form = CustomUserLoginForm(data=request.POST)
		
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = auth.authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("Your account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied. Get back to the <a href=\"/\">homepage</a>.")
			
	else:
		# login_form = CustomUserLoginForm()
		return render(request, 'login.html')
		
	# return render(request, 'login.html', {'login_form': login_form})
	return render(request, 'login.html')
'''

def login(request):
	c = {}
	c.update(csrf(request))
	return render(request, 'login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/login')
		
def loggedin(request):
	return render(request, 'loggedin.html',
				  {'user': request.user})
				  
def loggedout(request):
	return render(request, 'invalid_login.html')
