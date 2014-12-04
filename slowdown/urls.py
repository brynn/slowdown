from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),


    url(r'^$', 'accounts.views.home'),
    url(r'^login/$', 'accounts.views.home'),
    url(r'^logout/$', 'accounts.views.logout'),
    url(r'^signup/$', 'accounts.views.signup'),
    url(r'^examples/$', 'accounts.views.examples'),
    url(r'^unsubscribe/$', 'accounts.views.unsubscribe'),
    url(r'^done/$', 'accounts.views.done', name='done'),
    
    url(r'^check-and-send-email/$', 'accounts.views.check_and_send_email'),
    url(r'^edit-settings/$', 'accounts.views.edit_settings'),
    
    url(r'^i/(\S+)/$', 'accounts.views.item_permalink'),
    
#     url(r'^add-urls/$', 'accounts.views.add_urls'),
)

