from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog import views
from allauth.account.views import confirm_email

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    #url(r'^accounts/login/$', views.LoginUser.as_view(template_name="login.html")),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'', include('blog.urls')),
    url('^markdown/', include('django_markdown.urls')),
)
