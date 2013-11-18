from django.contrib import admin
from patrickbeeson.apps.media.models import Photo

class PhotoAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'slug')
	search_fields = ('title', 'caption')

admin.site.register(Photo, PhotoAdmin)