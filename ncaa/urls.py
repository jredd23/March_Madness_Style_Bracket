from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from march_madness import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ncaa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('march_madness.urls')),
    url(r'^create/', views.create, name='create'),
    url(r'^login/', include('registration.backends.simple.urls')),
    url(r'^register', views.register, name='register'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^print/', views.printout, name='print'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^rules/', views.rules, name='rules'),
    url(r'^site-admin/', views.admin, name='admin'),
    url(r'^update_site/', views.update_site, name='update_site'),
    url(r'^update_ff/', views.update_ff, name='update_ff'),
    url(r'^update_r64_r1/', views.update_r64_r1, name='update_r64_r1'),
    url(r'^update_r64_r2/', views.update_r64_r2, name='update_r64_r2'),
    url(r'^update_r64_r3/', views.update_r64_r3, name='update_r64_r3'),
    url(r'^update_r64_r4/', views.update_r64_r4, name='update_r64_r4'),
    url(r'^update_rules_edit/', views.update_rules_edit, name='update_rules_edit'),
    url(r'^update_rules_new/', views.update_rules_new, name='update_rules_new'),
    url(r'^update_rules_edit_change/', views.update_rules_edit_change, name='update_rules_edit_change'),
    url(r'^update_rules_del_change/', views.update_rules_del_change, name='update_rules_del_change'),
    url(r'^update_rules_del/', views.update_rules_del, name='update_rules_del'),
)
urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                    'document_root': settings.MEDIA_ROOT}))
