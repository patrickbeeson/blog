from django.views.generic.simple import direct_to_template
from patrickbeeson.apps.blog.models import Entry

def home_page(request):
	return direct_to_template(
		request,
		extra_context={'entry_list': Entry.live.all().order_by('-pub_date')[:6]},
		template = 'home.html',
	)
