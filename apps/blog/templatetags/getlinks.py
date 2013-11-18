from django import template

def getlinks(value):
	"""
	Returns links found in an (X)HTML string as Python objects for itteration in templates.
   
	EXAMPLE:
	
		<ul>
		{% for link in blog.entry.body|getlinks %}
		<li><a href="{{ link.href }}">{{ link.title }}</a></li>
		{% endfor %}
		</ul>

	"""
	try:
		from BeautifulSoup import BeautifulSoup
	except ImportError:
		if settings.DEBUG:
			raise template.TemplateSyntaxError, "Error in {% getlinks %} filter: The Python BeautifulSoup and/or urllib2 libraries aren't installed."
		return value
	else:
		soup = BeautifulSoup(value)
		return soup.findAll('a')
register = template.Library()
register.filter(getlinks)
