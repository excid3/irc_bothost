from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Dashboard
    (r'^$', 'website.front.views.front_front'),

    # Static content
    (r'^static(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT}),

    # Login
    (r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login/login.html'}),
    (r'^logout$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^signup$', 'website.login.views.login_signup'),

    # User views
    (r'^bots/new$', 'website.common.views.common_new'),
    (r'^bots/(\d+)$', 'website.common.views.common_bot'),    
    (r'^bots/(\d+)/edit$', 'website.common.views.common_edit'),
    (r'^bots/(\d+)/edit/delete$', 'website.common.views.common_delete'),

    # API
    #(r'^api/updates$', 'website.common.views.common_update'),
    
    # Admin
    (r'^admin/doc$', include('django.contrib.admindocs.urls')),
    (r'^admin$', include(admin.site.urls)),

    (r'^bot-admin$', 'website.admin.views.admin_dashboard'),
    (r'^bot-admin/shutdown$', 'website.admin.views.admin_shutdown'),
)
