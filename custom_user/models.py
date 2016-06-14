from django.db import models
from time import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlquote
from datetime import datetime
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from resizeimage import resizeimage

from stdimage.models import StdImageField


class CustomUserManager(BaseUserManager):
	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		now = datetime.now()
		
		if not email:
			raise ValueError("The given email must be set")
		
		email = self.normalize_email(email)
		user = self.model(email=email,
						  is_staff=is_staff, is_active=True,
						  is_superuser=is_superuser, last_login=now,
						  date_joined=now, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
		
	def create_user(self, email, password=None, **extra_fields):
		return self._create_user(email, password, False, False, **extra_fields)
		
	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, password, True, True, **extra_fields)


def upload_avatar_to(instance, filename):
		import os
		from django.utils.timezone import now
		filename_base, filename_ext = os.path.splitext(filename)
		return 'media/images/avatars/%s%s' % (
			now().strftime("%Y%m%d%H%M%S"),
			filename_ext.lower(),
		)

class CustomUser(AbstractBaseUser, PermissionsMixin):
	first_name 	   = models.CharField(max_length=254, blank=True)
	second_name    = models.CharField(max_length=254, blank=True)
	email 		   = models.EmailField(blank=True, unique=True)
	date_joined    = models.DateTimeField(_('date joined'), default=datetime.now())
	#avatar 		   = models.ImageField('profile picture', upload_to=upload_avatar_to, null=True, blank=True)
	_avatar		   = StdImageField(upload_to=upload_avatar_to, null=True, blank=True, db_column='avatar',
								   variations={
								       'thumbnail': {'width': 250, 'height': 250, "crop": True}
								   })
	is_active      = models.BooleanField(default=False)
	is_admin       = models.BooleanField(default=False)
	is_staff       = models.BooleanField(default=False)
	
	@property
	def avatar(self):
		return self._avatar

	@avatar.setter
	def avatar(self, value):
		self._avatar = value
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'second_name']
	
	objects = CustomUserManager()
	
	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
	
	def save(self, *args, **kwargs):
		super(CustomUser, self).save(*args, **kwargs)
	
	'''
		self.create_avatar_thumb()
		
	def create_avatar_thumb(self):
		import os
		from PIL import Image
		from django.core.files.storage import default_storage as storage
		if not self.avatar:
			return ""
		file_path = self.avatar.name
		filename_base, filename_ext = os.path.splitext(file_path)
		thumb_file_path = "%s_thumb.jpg" % filename_base
		if storage.exists(thumb_file_path):
			return "exists"
		try:
			# resize the original image and return url path of the thumbnail
			f = storage.open(file_path, 'r')
			image = Image.open(f)
			width, height = image.size
			
			if width > height:
				delta = width - height
				left = int(delta/2)
				upper = 0
				right = height + left
				lower = height
			else:
				delta = height - width
				left = 0
				upper = int(delta/2)
				right = width
				lower = width + upper
				
			image = image.crop((left, upper, right, lower))
			image = image.resize((250, 250), Image.ANTIALIAS)
			
			f_thumb = storage.open(thumb_file_path, "w")
			image.save(f_thumb, "JPEG")
			f_thumb.close()
			return "success"
		except:
			return "error"

	def get_avatar_thumb_url(self):
		import os
		from django.core.files.storage import default_storage as storage
		if not self.avatar:
			return ""
		file_path = self.avatar.name
		filename_base, filename_ext = os.path.splitext(file_path)
		thumb_file_path = "%s_thumb.jpg" % filename_base
		if storage.exists(thumb_file_path):
			return storage.url(thumb_file_path)
		return ""
		
	
	def save(self, *args, **kwargs):
		if self.avatar:
			pil_image_obj = Image.open(self.avatar)
			new_image = resizeimage.resize_width(pil_image_obj, 300, validate=False)

			new_image_io = BytesIO()
			new_image.save(new_image_io, format='JPEG')

			temp_name = self.avatar.name
			self.avatar.delete(save=False)

			self.avatar.save(
				temp_name,
				content=ContentFile(new_image_io.getvalue()),
				save=False
			)
			
		super(CustomUser, self).save(*args, **kwargs)
	'''
	
	def get_absolute_url(self):
		return "/users/%s" % urlquote(self.email)
		
	def get_full_name(self):
		"""
		Returns the first_name plus the last_name, with a space in between.
		"""
		return self.email
		
	def __str__(self):
		return self.email
		
	def get_short_name(self):
		"""
		Returns the first name for the user.
		"""	
		return self.first_name
		
	def email_user(self, subject, message, from_email=None):
		"""
		Sends an email to this user.
		"""
		send_email(subject, message, from_email, [self.email])
        
