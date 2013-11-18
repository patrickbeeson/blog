from django.contrib import admin
from patrickbeeson.apps.blog.models import Entry, Tag

class TagAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('slug', 'title')

class EntryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('response_link', 'centerpiece_image')
	list_display = ('title', 'slug', 'pub_date', 'update', 'status')
	list_filter = ('status', 'tags', 'pub_date',)
	search_fields = ('title', 'meta_description', 'body', 'meta_keywords')	

admin.site.register(Tag, TagAdmin)
admin.site.register(Entry, EntryAdmin)