from django.conf.urls.defaults import *
#from patrickbeeson.apps.media.models import Photo
from patrickbeeson.apps.blog.feeds import BlogEntryFeed, LatestEntriesByTag, CommentsForEntry
from django.contrib.comments.feeds import LatestCommentFeed
from django.contrib.sitemaps import FlatPageSitemap
from patrickbeeson.sitemaps import BlogSitemap
from patrickbeeson.robots import robots_txt
from django.contrib import admin
from patrickbeeson import views

admin.autodiscover()

#def get_live_entries():
#	return Entry.live.all()

sitemaps = {
	'blog': BlogSitemap,
    'flatpages': FlatPageSitemap,
}

#comments_info_dict = {
#	'queryset': FreeComment.objects.filter(is_public=True),
#	'paginate_by': 15,
#}

#photo_list_info = {
#	'queryset': Photo.objects.all(),
#	'allow_empty': True,
#}

#photo_detail_info = {
#	'queryset': Photo.objects.all(),
#	'template_object_name': 'photo',
#}

urlpatterns = patterns('',
	# Robots
	(r'^robots.txt$', robots_txt),
	# Admin
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	('^admin/(.*)', admin.site.root),
	# Home page
	#(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),
	(r'^$', 'patrickbeeson.views.home_page'),
	# Photos
	#(r'^photos/$', 'django.views.generic.list_detail.object_list', photo_list_info),
	#(r'^photo/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', photo_detail_info),
	# Comments
	#(r'^comments/$', 'django.views.generic.list_detail.object_list', comments_info_dict),
	(r'^comments/', include('django.contrib.comments.urls')),
	# Contact form
	(r'^contact/', include('contact_form.urls')),
	# Feeds
	(r'^feeds/blog/$', BlogEntryFeed()),
	(r'^feeds/tags/(?P<slug>[-\w]+)/$', LatestEntriesByTag()),
	(r'^feeds/entry-comments/(?P<slug>[-\w]+)/$', CommentsForEntry()),
	(r'^feeds/comments/$', LatestCommentFeed()),
	# Shortcut URLs
	(r'^r/', include('django.conf.urls.shortcut')),
	# Sitemaps
	(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	(r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	# Blog
	(r'^blog/', include('patrickbeeson.apps.blog.urls')),
	# ShortURL
#	('^s/', include('shorturls.urls')),
	# Flat pages
	(r'', include('django.contrib.flatpages.urls')),
)
