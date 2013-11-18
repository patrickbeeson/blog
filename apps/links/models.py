from django.db import models

class Link(models.Model):
	title = models.CharField(max_length=200)
	url = models.URLField()
	
	class Meta:
		verbose_name_plural = 'links'
		
	def __unicode__(self):
		return self.title