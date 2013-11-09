#from django.conf.urls.defaults import *
from django.conf.urls.defaults import include
from django.conf.urls import patterns, url
from django.contrib import admin
import dbindexer

from healthplans.views import ProviderListView
from healthplans.views import ProviderDetailView
from healthplans.views import PlanListView
from healthplans.views import PlanDetailView

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),
    ('^admin/', include(admin.site.urls)),

    url(r'^providers/$', ProviderListView.as_view(), name='provider-list'),
    url(r'^providers/(?P<slug>[\w-]+)$', ProviderDetailView.as_view(), name='provider-detail'),
    url(r'^plans/$', PlanListView.as_view(), name='plan-list'),
    url(r'^plans/(?P<slug>[\w-]+)$', PlanDetailView.as_view(), name='plan-detail'),
)
