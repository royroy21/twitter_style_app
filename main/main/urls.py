# Django Imports
from django.conf.urls import patterns, include, url
from django.contrib import admin
from twitter_style_app_1.views import register_new_user
from twitter_style_app_1.views import user_login
from twitter_style_app_1.views import user_logout
from twitter_style_app_1.views import new_status
from twitter_style_app_1.views import follow_user
from twitter_style_app_1.views import view_time_line


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # twitter style app urls
    url(r'^register_new_user/', register_new_user),
    url(r'^user_login/', user_login),
    url(r'^user_logout/', user_logout),
    url(r'^new_status/', new_status),
    url(r'^follow_user/(?P<this_user_id>[^/]+)/(?P<user_to_follow_id>[^/]+)/', follow_user),
    url(r'^view_time_line/(?P<user_id>[^/]+)/', view_time_line),
)