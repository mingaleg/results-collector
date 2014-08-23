from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^(grade/(?P<grade>\d+)/)?$', 'collector.views.glob', name='glob'),
    url(r'^(grade/(?P<grade>\d+)/)?page/(?P<page>\d+)$', 'collector.views.table_glob', name='table_glob'),
    url(r'^regions', 'collector.views.regions', name='regions'),
    url(r'^global.csv$', 'collector.views.globcsv', name='globcsv'),
    url(r'^region/(?P<reg>.*?)/(grade/(?P<grade>\d+)/)?page/(?P<page>\d+)$', 'collector.views.table_reg', name='table_reg'),
    url(r'^region/(?P<reg>.*?)(/grade/(?P<grade>\d+))?/$', 'collector.views.regionres', name='regionres'),
    url(r'^(?P<reg>.*?).csv$', 'collector.views.regionres', name='regioncsv'),


    url(r'^admin/collector/massregionresults/(?P<pk>\d+?)/apply/$', "collector.views.apply_mass", name="massapply"),
    # url(r'^results_collector/', include('results_collector.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
