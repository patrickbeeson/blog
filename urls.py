from django.conf.urls.defaults import *
from patrickbeeson.apps.blog.feeds import BlogEntryFeed, LatestEntriesByTag, CommentsForEntry
from django.contrib.comments.feeds import LatestCommentFeed
from django.contrib.sitemaps import FlatPageSitemap
from patrickbeeson.sitemaps import BlogSitemap
from patrickbeeson.robots import robots_txt
from django.contrib import admin
from patrickbeeson import views

admin.autodiscover()

sitemaps = {
	'blog': BlogSitemap,
    'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
	# Robots
	(r'^robots.txt$', robots_txt),
	
	# Admin
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	('^admin/(.*)', admin.site.root),
	
	# Home page
	(r'^$', 'patrickbeeson.views.home_page'),

	# Comments
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

	# Flat pages
	(r'', include('django.contrib.flatpages.urls')),
)
