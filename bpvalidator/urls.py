from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from bpvalidator import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'bpvalidator.views.render', {"page":"index"}),
    url(r'^(?P<page>\w+)$', 'bpvalidator.views.render'),

    url(r'^api/validity/test/?$', 'bpvalidator.bp.check', name='test'),

    # Admin Console
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

