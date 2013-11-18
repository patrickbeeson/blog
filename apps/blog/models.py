import datetime
#from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google
from patrickbeeson.apps.media.models import Photo
from patrickbeeson.apps.links.models import Link
from markdown import markdown
from django.contrib.comments.signals import comment_was_posted
from django.utils.encoding import smart_str
from django.core.mail import mail_managers
import akismet
from django.conf import settings
from django.contrib.sites.models import Site

class LiveEntryManager(models.Manager):
	def get_query_set(self):
		return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Tag(models.Model):
	slug = models.SlugField(unique=True)
	title = models.CharField(max_length=50, help_text='This field will populate the slug field. Maximum 50 characters.')
	description = models.TextField(help_text='Please use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.')
	description_html = models.TextField(editable=False, blank=True)
	
	class Meta:
		verbose_name_plural = 'tags'
	
	def __unicode__(self):
		return self.title
		
	def live_entry_set(self):
		"""
		Returns only entries with a status of live.
		"""
		return self.entry_set.filter(status=Entry.LIVE_STATUS)

	def save(self):
		self.description_html = markdown(self.description)
		super(Tag, self).save()
	
	def get_absolute_url(self):
		return '/blog/tags/%s/' % (self.slug)

#class TagAdmin(admin.ModelAdmin):
#	prepopulated_fields = {"slug": ("title",)}
#	list_display = ('slug', 'title')

class Entry(models.Model):
	# Status options
	CLOSED_STATUS = 1
	EDITING_STATUS = 2
	LIVE_STATUS = 3
	STATUS_CHOICES = (
		(CLOSED_STATUS, 'Closed'),
		(EDITING_STATUS, 'Editing'),
		(LIVE_STATUS, 'Public'),
	)
	# Title and slug fields
	title = models.CharField(max_length=200, help_text='This field will populate the slug field. Maximum 200 characters.')
	slug = models.SlugField(unique_for_date='pub_date')
	
	# Summary and body fields
	summary = models.TextField(help_text='Please use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.')
	body = models.TextField(help_text='Please use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.')

	# Markdown conversion for summary and body fields
	summary_html = models.TextField(editable=False, blank=True)
	body_html = models.TextField(editable=False, blank=True)
	
	# Tag field
	tags = models.ManyToManyField(Tag, blank=True)
	
	# Meta fields
	meta_keywords = models.CharField(blank=True, max_length=300, help_text='Comma-separated list of keyworks for this entry. Maximum 300 characters.')
	meta_description = models.CharField(blank=True, max_length=400, help_text='A brief description of this entry. Maximum 400 characters.')
	
	# Image field
	centerpiece_image = models.ForeignKey(Photo, blank=True, null=True)
	
	# Response link field
	response_link = models.ForeignKey(Link, blank=True, null=True)
	
	# Date fields
	pub_date = models.DateTimeField(default=datetime.datetime.now)
	update = models.DateTimeField(blank=True, editable=True, auto_now=False, null=True)
	
	# Author field
	author = models.ForeignKey(User)
	
	# Enable comments field
	enable_comments = models.BooleanField(default=True)
	
	# Entry status field
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=EDITING_STATUS)
	
	# Entry managers
	objects = models.Manager()
	live = LiveEntryManager()
		
	class Meta:
		ordering = ['-pub_date']
		verbose_name_plural = 'entries'
	
	def __unicode__(self):
		return self.title
		
	def save(self):
		self.summary_html = markdown(self.summary)
		self.body_html = markdown(self.body)
		super(Entry, self).save()
		try:
			ping_google()
		except Exception:
			pass
	
	def get_absolute_url(self):
		return '/blog/%s/%s/' % (self.pub_date.strftime('%Y/%b/%d').lower(), self.slug)

	def get_tags_with_entries(self):
		tags = self.tags.all()
		for tag in tags:
			tag.entries = tag.entry_set.exclude(id=self.id)[:5]
		return tags

	@property
	def related_entry_set(self):
		tag_id_list = self.tags.values_list('id', flat=True)
		return Entry.live.filter(tags__id__in=tag_id_list).exclude(id=self.id).distinct()[:10]
		
	@property
	def comments_expired(self):
		delta = datetime.datetime.now() - self.pub_date
		return delta.days < 60

def moderate_comment(sender, comment, request, **kwargs):
	ak = akismet.Akismet(
		key = settings.AKISMET_API_KEY,
		blog_url = 'http://%s/' % Site.objects.get_current().domain
	)
	data = {
		'user_ip': request.META.get('REMOTE_ADDR', ''),
		'user_agent': request.META.get('HTTP_USER_AGENT', ''),
		'referrer': request.META.get('HTTP_REFERRER', ''),
		'comment_type': 'comment',
		'comment_author': smart_str(comment.user_name),
	}
	if ak.comment_check(smart_str(comment.comment), data=data, build_data=True):
		comment.is_public = False
		comment.save()
	
	if comment.is_public:	
		email_body = "%s"
		mail_managers ("New comment posted", email_body % (comment.get_as_text()))
	
comment_was_posted.connect(moderate_comment)
	
#class EntryAdmin(admin.ModelAdmin):
#	prepopulated_fields = {"slug": ("title",)}
#	raw_id_fields = ('response_link', 'centerpiece_image')
#	list_display = ('title', 'slug', 'pub_date', 'update', 'status')
#	list_filter = ('status', 'tags', 'pub_date',)
#	search_fields = ('title', 'meta_description', 'body', 'meta_keywords')	

#admin.site.register(Tag, TagAdmin)
#admin.site.register(Entry, EntryAdmin)