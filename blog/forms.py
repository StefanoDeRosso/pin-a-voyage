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
		
		instance.generate_unique_slug()
			
		instance.save()
		
		return instance
		
	def save_to_draft(self):
		instance = super(PostForm, self).save(commit=False)
		
		instance.generate_unique_slug()
		
		return instance

class CommentForm(forms.ModelForm):
	
	class Meta:
		model = Comment
		fields = ('text',)

