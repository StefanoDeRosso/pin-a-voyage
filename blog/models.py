import itertools

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django_markdown.models import MarkdownField
from datetime import datetime
from custom_user.models import CustomUserManager, CustomUser
from blogproject import settings


class Tag(models.Model):
	slug = models.SlugField(max_length=200, unique=True)

	def __unicode__(self):
		return self.slug
		
	def get_absolute_url(self):
		return reverse("tag_index", kwargs={"slug": self.slug})

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	title = models.CharField(max_length=200)
	text = MarkdownField()
	slug = models.SlugField(unique=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	published_date = models.DateTimeField(blank=True, null=True)
	tags = models.ManyToManyField(Tag)
	
	@models.permalink
	def get_absolute_url(self):
		return 'blog:post', (self.slug,)
	
	def generate_unique_slug(self):
		slug = self._meta.get_field('slug')
		max_length = slug.max_length
		slug = orig = slugify(self.title)[:max_length]
		
		for x in itertools.count(1):
			if not Post.objects.filter(slug=slug).exists():
				break

			# Truncate the original slug dynamically. Minus 1 for the hyphen.
			slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
		
		self.slug = slug

	def save(self):
		self.published_date = timezone.now()
		self.generate_unique_slug()
		super(Post, self).save()
		
	def __unicode__(self):
		return self.title
		
	def approved_comments(self):
		return self.comments.filter(approved=True)

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
	created = models.DateTimeField(auto_now_add=True)
	approved = models.BooleanField(default=False)
	
	def approve(self):
		self.approved = True
		self.save()
		
	def __unicode__(self):
		return self.author
		return self.text
