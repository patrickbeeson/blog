from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.views.generic import date_based, list_detail
from patrickbeeson.apps.blog.models import *

import datetime
import re


def entry_list(request, page=0):
  """
  Entry list

  Template: ``blog/entry_list.html``
  Context:
	  object_list
		  list of objects
	  is_paginated
		  are the results paginated?
	  results_per_page
		  number of objects per page (if paginated)
	  has_next
		  is there a next page?
	  has_previous
		  is there a prev page?
	  page
		  the current page
	  next
		  the next page
	  previous
		  the previous page
	  pages
		  number of pages, total
	  hits
		  number of objects, total
	  last_on_page
		  the result number of the last of object in the
		  object_list (1-indexed)
	  first_on_page
		  the result number of the first object in the
		  object_list (1-indexed)
	  page_range:
		  A list of the page numbers (1-indexed).
  """
  return list_detail.object_list(
	request,
	queryset = Entry.live.all(),
	paginate_by = 20,
	page = page,
  )

def entry_archive_year(request, year):
  """
  Entry archive year

  Templates: ``blog/entry_archive_year.html``
  Context:
	date_list
	  List of months in this year with objects
	year
	  This year
	object_list
	  List of objects published in the given month
	  (Only available if make_object_list argument is True)
  """
  return date_based.archive_year(
	request,
	year = year,
	date_field = 'pub_date',
	queryset = Entry.live.all(),
	make_object_list = True,
  )

def entry_archive_month(request, year, month):
  """
  Entry archive month

  Templates: ``blog/entry_archive_month.html``
  Context:
	month:
	  (date) this month
	next_month:
	  (date) the first day of the next month, or None if the next month is in the future
	previous_month:
	  (date) the first day of the previous month
	object_list:
	  list of objects published in the given month
  """
  return date_based.archive_month(
	request,
	year = year,
	month = month,
	date_field = 'pub_date',
	queryset = Entry.live.all(),
  )

def entry_archive_day(request, year, month, day):
  """
  Entry archive day

  Templates: ``blog/entry_archive_day.html``
  Context:
	object_list:
	  list of objects published that day
	day:
	  (datetime) the day
	previous_day
	  (datetime) the previous day
	next_day
	  (datetime) the next day, or None if the current day is today
  """
  return date_based.archive_day(
	request,
	year = year,
	month = month,
	day = day,
	date_field = 'pub_date',
	queryset = Entry.live.all(),
  )

def entry_detail(request, slug, year, month, day):
  """
  Entry detail

  Templates: ``blog/entry_detail.html``
  Context:
	object:
	  the object to be detailed
  """
  return date_based.object_detail(
	request,
	year = year,
	month = month,
	day = day,
	date_field = 'pub_date',
	slug = slug,
	template_object_name = 'entry',
	queryset = Entry.live.all(),
  )

def tag_list(request):
  """
  Tag list

  Template: ``blog/tag_list.html``
  Context:
	object_list
	  List of categories.
  """
  return list_detail.object_list(
	request,
	queryset = Tag.objects.all(),
	template_name = 'blog/tag_list.html',
  )
 
def tag_detail(request, slug):
  """
  Tag detail
  
  Template: ``blog/tag_detail.html``
  Context:
    object_list
      List of entries specific to the given tag.
    tag
      Given tag.
  """
  try:
    tag = Tag.objects.get(slug__iexact=slug)
  except Tag.DoesNotExist:
    raise Http404
  
  return list_detail.object_list(
    request,
    queryset = tag.live_entry_set(),
    extra_context = { 'tag': tag },
    template_name = 'blog/tag_detail.html',
  )


# Stop Words courtesy of http://www.dcs.gla.ac.uk/idom/ir_resources/linguistic_utils/stop_words
STOP_WORDS = r"""\b(a|about|above|across|after|afterwards|again|against|all|almost|alone|along|already|also|
although|always|am|among|amongst|amoungst|amount|an|and|another|any|anyhow|anyone|anything|anyway|anywhere|are|
around|as|at|back|be|became|because|become|becomes|becoming|been|before|beforehand|behind|being|below|beside|
besides|between|beyond|bill|both|bottom|but|by|call|can|cannot|cant|co|computer|con|could|couldnt|cry|de|describe|
detail|do|done|down|due|during|each|eg|eight|either|eleven|else|elsewhere|empty|enough|etc|even|ever|every|everyone|
everything|everywhere|except|few|fifteen|fify|fill|find|fire|first|five|for|former|formerly|forty|found|four|from|
front|full|further|get|give|go|had|has|hasnt|have|he|hence|her|here|hereafter|hereby|herein|hereupon|hers|herself|
him|himself|his|how|however|hundred|i|ie|if|in|inc|indeed|interest|into|is|it|its|itself|keep|last|latter|latterly|
least|less|ltd|made|many|may|me|meanwhile|might|mill|mine|more|moreover|most|mostly|move|much|must|my|myself|name|
namely|neither|never|nevertheless|next|nine|no|nobody|none|noone|nor|not|nothing|now|nowhere|of|off|often|on|once|
one|only|onto|or|other|others|otherwise|our|ours|ourselves|out|over|own|part|per|perhaps|please|put|rather|re|same|
see|seem|seemed|seeming|seems|serious|several|she|should|show|side|since|sincere|six|sixty|so|some|somehow|someone|
something|sometime|sometimes|somewhere|still|such|system|take|ten|than|that|the|their|them|themselves|then|thence|
there|thereafter|thereby|therefore|therein|thereupon|these|they|thick|thin|third|this|those|though|three|through|
throughout|thru|thus|to|together|too|top|toward|towards|twelve|twenty|two|un|under|until|up|upon|us|very|via|was|
we|well|were|what|whatever|when|whence|whenever|where|whereafter|whereas|whereby|wherein|whereupon|wherever|whether|
which|while|whither|who|whoever|whole|whom|whose|why|will|with|within|without|would|yet|you|your|yours|yourself|
yourselves)\b"""


def search(request):
  """
  Search for blog entries.
  
  This template will allow you to setup a simple search form that will try to return results based on
  given search strings. The queries will be put through a stop words filter to remove words like
  'the', 'a', or 'have' to help imporve the result set.
  
  Template: ``blog/entry_search.html``
  Context:
	object_list
	  List of blog entries that match given search term(s).
	search_term
	  Given search term.
  """
  if request.GET:
	stop_word_list = re.compile(STOP_WORDS, re.IGNORECASE)
	search_term = '%s' % request.GET['q']
	cleaned_search_term = stop_word_list.sub('', search_term)
	cleaned_search_term = cleaned_search_term.strip()
	if len(cleaned_search_term) != 0:
	  entry_list = Entry.objects.filter(body__icontains=cleaned_search_term, status__gte=2, pub_date__lte=datetime.datetime.now())
	  context = { 'object_list': entry_list, 'search_term':search_term }
	  return render_to_response('blog/entry_search.html', context, context_instance=RequestContext(request))
	else:
	  message = 'Search term was too vague. Please try again.'
	  context = { 'message':message }
	  return render_to_response('blog/entry_search.html', context, context_instance=RequestContext(request))
  else:
	return render_to_response('blog/entry_search.html', {}, context_instance=RequestContext(request))
