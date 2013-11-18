from django.contrib import admin
from patrickbeeson.apps.links.models import Link

class LinkAdmin(admin.ModelAdmin):
	list_display = ('title', 'url')

admin.site.register(Link, LinkAdmin)