#from django.contrib import admin
from django.db import models
import datetime

class Photo(models.Model):
	pub_date = models.DateTimeField()
	title = models.CharField(max_length=50)
	slug = models.SlugField(unique=True, help_text='Slug prepopulates from title')
	photo = models.ImageField(upload_to='images/photos', width_field='photo_width', height_field='photo_height')
	caption = models.TextField()
	credit = models.CharField(max_length=100, help_text='If you wish to give credit to a photographer, add their name here.', blank=True)
	photo_width = models.IntegerField(help_text='The photo width in pixels. Please use 262 pixels width for blog entry photos.')
	photo_height = models.IntegerField(help_text='The photo height in pixels.')
	flickr_url = models.URLField(help_text='If the photo is located on Flickr, add the URL here.', blank=True)
	
	class Meta:
		verbose_name_plural = 'photos'

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return '/photo/%s/%s/' % (self.pub_date.strftime('%Y/%b/%d').lower(), self.slug)

#class PhotoAdmin(admin.ModelAdmin):
#	prepopulated_fields = {"slug": ("title",)}
#	list_display = ('title', 'slug')
#	search_fields = ('title', 'caption')

#admin.site.register(Photo, PhotoAdmin)