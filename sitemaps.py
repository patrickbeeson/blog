from django.contrib.sitemaps import Sitemap
from patrickbeeson.apps.blog.models import Entry
import datetime

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Entry.objects.filter(status=3)

	def lastmod(self, obj):
		return obj.pub_date

	def location(self, obj):
		return "/blog/%s" % obj.slug 