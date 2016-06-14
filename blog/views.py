from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseBadRequest, Http404
from django.conf import settings
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .models import *
#from .models import Post, Comment, CustomUserManager, CustomUser, UserProfile
from forms import PostForm, CommentForm
from django.contrib.auth import update_session_auth_hash
from custom_user.forms import CustomUserCreationForm, CustomUserChangeForm, CustomLoginForm, PasswordChangeForm, SignupForm
from custom_user.backends import CustomUserAuth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, authenticate
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.conf import settings
from django.core import serializers, signing
from django.core.mail import send_mail, EmailMultiAlternatives
import hashlib, datetime, random
import json
from django.core.serializers.json import DjangoJSONEncoder
from allauth.account.signals import user_signed_up, email_confirmed
from django.dispatch import receiver
from allauth.account.models import EmailAddress


class TagIndex(ListView):
	template_name = 'blog/post_list.html'
	paginate_by = 5
	context_object_name = 'posts'
	
	def get_queryset(self):
		slug = self.kwargs['slug']
		tag = Tag.objects.get(slug=slug)
		results = Post.objects.filter(tags=tag)
		return results

def register(request):
	
	if request.method == 'POST':
		user_form = CustomUserCreationForm(request.POST)
		
		if user_form.is_valid():
			user = user_form.save()
			
			email = user_form.cleaned_data['email']
			first_name = user_form.cleaned_data['first_name']
			salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
			activation_key = hashlib.sha1(salt+email).hexdigest()            
			key_expires = datetime.datetime.today() + datetime.timedelta(2)
			
			user=CustomUser.objects.get(email=email)
            
			new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
			new_profile.save()
			
			email_subject = 'Account confirmation - Pin a Voyage'
			email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
			48hours https://pin-a-voyage.herokuapp.com/activate/%s" % (first_name, activation_key)

			send_mail(email_subject, email_body, 'voyage.pin@gmail.com', [email], fail_silently=False)

			return render(request, 'blog/registered.html')
			
		else:
			print user_form.errors
	else:
		user_form = CustomUserCreationForm()
	
	return render(request, 'blog/post_list.html', {'user_form': user_form})

def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
	if request.user.is_authenticated():
		HttpResponseRedirect('../')

    # check if there is UserProfile which matches the activation key (if not then display 404)
	user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
	if user_profile.key_expires < timezone.now():
		return HttpResponse("The activation key has expired. You can get back to the <a href='../'>homepage</a> and register again.")
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
	user = user_profile.user
	user.is_active = True
	user.save()
	
	return render_to_response('blog/activation_success_view.html')

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):

    user.is_active = True
    user.is_staff = False

    user.save()

@login_required
def update_profile(request):
	#args = {}
	email = request.user.email
	first_name = request.user.first_name
	second_name = request.user.second_name

	if request.method == 'POST':
		edit_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
		
		if edit_form.is_valid():
			edit_form.save()
			messages.success(request, 'Profile correctly updated')
		else:
			HttpResponse("Invalid details supplied. Get back to the <a href=\"../\">edit page</a>.")
	else:
		edit_form = CustomUserChangeForm(initial={'email': email, 'first_name': first_name, 'second_name': second_name})
		
	#args['form'] = edit_form
	return render(request, 'blog/user_edit.html', {'edit_form': edit_form})

@login_required
def update_password(request):
	password_form = PasswordChangeForm(user=request.user)
	success = False
	ajax_vars = {'success': success}
	json_data = json.dumps(ajax_vars)
	print json_data
	
	if request.method == 'POST':
		password_form = PasswordChangeForm(user=request.user, data=request.POST)
		if password_form.is_valid():
			password_form.save()
			update_session_auth_hash(request, password_form.user)
			success = True
			ajax_vars = {'success': success}
			json_data = json.dumps(ajax_vars)
			print json_data
			messages.success(request, 'Password correctly updated')

	return render(request, 'blog/password.html', {
		'password_form': password_form,
		'json_data': json_data,
	})

def login(request):
	if request.method == 'POST':
		login_form = CustomLoginForm(request.POST)
		
		email = request.POST.get('email')
		password = request.POST.get('password1')
		
		user = authenticate(email=email, password=password)
		
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("Your Pin a Voyage account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(email, password)
			return HttpResponse("Invalid login details supplied. Get back to the <a href=\"/\">homepage</a>.")
	else:
		login_form = CustomLoginForm()
		
	return render(request, 'blog/post_list.html', {})

@requires_csrf_token
def email_check(request):
    email = request.POST.get('email', False)
    if request.is_ajax():
        if email:
            query_email = CustomUser.objects.filter(email=email)
            if query_email.exists():
                #res = "{0} is already in use.".format(email)
                res = 404
            else:
                res = "This E-mail is ok."
            ajax_vars = {'response': res, 'email': email}
            json_data = json.dumps(ajax_vars)
        else:
            res = "This field is required."
            ajax_vars = {'response': res, 'email': email}
            json_data = json.dumps(ajax_vars)

        return HttpResponse(json_data, content_type='application/json')
        
@requires_csrf_token
def password_check(request):
	email = request.POST.get('email', False)
	password = request.POST.get('password', False)
    
	user = authenticate(email=email, password=password)
    
	if request.is_ajax():
		if password:
			query_password = CustomUser.objects.filter(password=password)
			if user:
				res = ""
			else:
				res = "&#8226; The e-mail or password you entered isn't correct."
			ajax_vars = {'response': res, 'password': password}
			json_data = json.dumps(ajax_vars)
		else:
			res = ""
			ajax_vars = {'response': res, 'password': password}
			json_data = json.dumps(ajax_vars)

		return HttpResponse(json_data, content_type='application/json')

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	user = CustomUser.objects.all()

	user_form = CustomUserCreationForm()
	login_form = CustomLoginForm()

	return render(request, 'blog/post_list.html', {'posts': posts, 'user_form': user_form, 'login_form': login_form, 'users': user})
	
def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	user_form = CustomUserCreationForm()
	login_form = CustomLoginForm()
	return render(request, 'blog/post_detail.html', {'post': post, 'user_form': user_form, 'login_form': login_form})
	
def add_comment_to_post(request, slug):
	post = get_object_or_404(Post, slug=slug)
	user_form = CustomUserCreationForm()
	login_form = CustomLoginForm()
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.post = post
			comment.save()
			return redirect('blog.views.post_detail', slug=post.slug)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form, 'user_form': user_form, 'login_form': login_form})

@login_required
def post_new(request):
	if request.method == "POST":
		if '_save' in request.POST:
			form = PostForm(request.POST)
			if form.is_valid():
				post = form.save()
				post.author = request.user
				post.published_date = timezone.now()
				post.save()
				form.save_m2m()
				return redirect('blog.views.post_detail', slug=post.slug)
		elif '_save_to_draft' in request.POST:
			form = PostForm(request.POST)
			if form.is_valid():
				post = form.save()
				post.author = request.user
				post.save()
				form.save_m2m()
				return redirect('blog.views.post_detail', slug=post.slug)
	else:
		form = PostForm()
			
	return render(request, 'blog/post_new.html', {'form': form})

@login_required	
def post_edit(request, slug):
	post = get_object_or_404(Post, slug=slug)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save()
			# Versione ok in locale 
			post.author = request.user
			# post.author = get_user(request)
			post.published_date = timezone.now()
			post.save()
			form.save_m2m()
			return redirect('blog.views.post_detail', slug=post.slug)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required	
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, slug):
	post = get_object_or_404(Post, slug=slug)
	post.publish()
	return redirect('blog.views.post_detail', slug=slug)

@login_required	
def post_remove(request, slug):
	post = get_object_or_404(Post, slug=slug)
	post.delete()
	return redirect('blog.views.post_list')

@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('blog.views.post_detail', slug=comment.post.slug)
	
@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	#post_slug = comment.post.slug
	comment.delete()
	return redirect('blog.views.post_detail', slug=comment.post.slug)

