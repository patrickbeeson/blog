from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site

from patrickbeeson.apps.blog.models import Entry, Tag

current_site = Site.objects.get_current()

import datetime

class BlogEntryFeed(Feed):
	description_template = 'feeds/blog_description.html'
	title_template = 'feeds/blog_title.html'
	title = "%s | The blog of Patrick Beeson" % current_site.name
	link = "http://patrickbeeson.com/"
	description = "I'm the director of digital communications for Wake Forest University in Winston-Salem, NC. I'm an avid cyclist, homebrewer, Web designer/developer, journalist and blogger."

	def items(self):
		return Entry.objects.filter(status=3, pub_date__lte=datetime.datetime.now())[:10]
		
	def item_title(self, item):
		return item.title
		
	def item_description(self, item):
		return item.description
		
class LatestEntriesByTag(Feed):
	description_template = 'feeds/tags_description.html'
	title_template = 'feeds/tags_title.html'
	def get_object(self, request, slug):
		return get_object_or_404(Tag, slug=slug)
		
	def title(self, obj):
		return "Entries for %s tag | %s" % (obj.title, current_site.name)
	
	def link(self, obj):
		if not obj:
			raise FeedDoesNotExist
		return obj.get_absolute_url()
	
	def description(self, obj):
		return "%s" % obj.description

	def items(self, obj):
		return Entry.objects.filter(tags__slug__exact=obj.slug, status=3).order_by('-pub_date')[:10]

class CommentsForEntry(Feed):
	def get_object(self, request, slug):
		return get_object_or_404(Entry, slug=slug)
	
	def title(self, obj):
		return "Comments posted on the entry %s | %s" % (obj.title, current_site.name)
	
	def link(self, obj):
		if not obj:
			raise FeedDoesNotExist
		return obj.get_absolute_url()
	
	def description(self, obj):
		return "Comments posted on the entry %s" % obj.title
	
	def items(self, obj):
		return Comment.objects.for_model(obj).filter(is_public=True, is_removed=False).order_by('-submit_date')[:15]