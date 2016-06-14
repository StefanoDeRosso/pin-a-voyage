from django.db import models
from django.conf import settings
from django.utils import timezone
from django_markdown.models import MarkdownField
from datetime import datetime
from custom_user.models import CustomUserManager, CustomUser
from blogproject import settings


class Tag(models.Model):
	slug = models.SlugField(max_length=200, unique=True)

	def __str__(self):
		return self.slug
		
	def get_absolute_url(self):
		return reverse("tag_index", kwargs={"slug": self.slug})

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	title = models.CharField(max_length=200)
	# text = models.TextField()
	text = MarkdownField()
	slug = models.SlugField(unique=True, default='post-title')
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	tags = models.ManyToManyField(Tag)
	
	@models.permalink
	def get_absolute_url(self):
		return 'blog:post', (self.slug,)
	
	def publish(self):
		self.published_date = timezone.now()
		self.save()
		
	def __unicode__(self):
		return self.title
		
	def approved_comments(self):
		return self.comments.filter(approved_comment=True)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.today())
      
    def __unicode__(self):
        return self.user.email

    class Meta:
        verbose_name_plural=u'User profiles'
		
class Comment(models.Model):
	post = models.ForeignKey('blog.Post', related_name='comments')
	author = models.CharField(max_length=200, default='author')
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	approved_comment = models.BooleanField(default=False)
	
	def approve(self):
		self.approved_comment = True
		self.save()
		
	def __unicode__(self):
		return self.text
