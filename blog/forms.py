import itertools

from django import forms
from .models import Post, Comment
from django.utils.text import slugify
from django_markdown.fields import MarkdownFormField
from django_markdown.widgets import MarkdownWidget
from django_markdown.models import MarkdownField

class PostForm(forms.ModelForm):
	
	text = MarkdownFormField()
    	
	class Meta:
		model = Post
		fields = (
			'title',
			'text',
			'tags'
		)
		
	def save(self):
		instance = super(PostForm, self).save(commit=False)
		
		max_length = Post._meta.get_field('slug').max_length
		instance.slug = orig = slugify(instance.title)[:max_length]
		
		for x in itertools.count(1):
			if not Post.objects.filter(slug=instance.slug).exists():
				break
				
			# Truncate the original slug dynamically. Minus 1 for the hyphen.
			instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
			
		instance.save()
		
		return instance
		
	def save_to_draft(self):
		instance = super(PostForm, self).save(commit=False)
		
		max_length = Post._meta.get_field('slug').max_length
		instance.slug = orig = slugify(instance.title)[:max_length]
		
		for x in itertools.count(1):
			if not Post.objects.filter(slug=instance.slug).exists():
				break
				
			# Truncate the original slug dynamically. Minus 1 for the hyphen.
			instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
		
		return instance

class CommentForm(forms.ModelForm):
	
	class Meta:
		model = Comment
		fields = ('text',)

