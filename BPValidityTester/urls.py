from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from BPValidityTester import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'BPValidityTester.views.render', {"page":"index"}),
    url(r'^(?P<page>\w+)$', 'BPValidityTester.views.render'),

    url(r'^api/validity/test/?$', 'BPValidityTester.bp.check', name='test'),

    # Admin Console
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

