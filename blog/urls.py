from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.post_list),
	url(r'^tag/(?P<slug>\S+)$', views.TagIndex.as_view(), name="tag_index"),
	url(r'^register', views.register),
	url(r'^activate/(?P<activation_key>\w+)/', views.register_confirm),
	url(r'^email_check', views.email_check),
	url(r'^password_check', views.password_check),
	url(r'^login', views.login),
	url(r'^edit/$', views.update_profile),
	url(r'^password-change/$', views.update_password),
	#url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^post/(?P<slug>[-_\w]+)/$', views.post_detail),
	#url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^post/(?P<slug>[-_\w]+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
	#url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
	#url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
	#url(r'^post/(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
	url(r'^post/(?P<slug>[-_\w]+)/publish/$', views.post_publish, name='post_publish'),
	url(r'^post/(?P<slug>[-_\w]+)/remove/$', views.post_remove, name='post_remove'),
	url(r'^post/(?P<slug>[-_\w]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
	url(r'^comment/(?P<pk>[0-9]+)/approve/$', views.comment_approve, name='comment_approve'),
	url(r'^comment/(?P<pk>[0-9]+)/remove/$', views.comment_remove, name='comment_remove'),
	#url(r'^comment/(?P<slug>[-_\w]+)/approve/$', views.comment_approve, name='comment_approve'),
	#url(r'^comment/(?P<slug>[-_\w]+)/remove/$', views.comment_remove, name='comment_remove'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
