from django.db import models
#from django.contrib import admin

class Link(models.Model):
	title = models.CharField(max_length=200)
	url = models.URLField()
	
	class Meta:
		verbose_name_plural = 'links'
		
	def __unicode__(self):
		return self.title

#class LinkAdmin(admin.ModelAdmin):
#	list_display = ('title', 'url')

#admin.site.register(Link, LinkAdmin)