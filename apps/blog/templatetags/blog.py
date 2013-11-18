from django import template
from django.core import template_loader
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
import re
from patrickbeeson.apps.blog.models import Entry, Tag
from django.template import Node

def do_get_month_list(parser, token):
    """
    Gets a list of months in which entries are published.
    
    Syntax::
    
    {% get_month_list %}
    """
    return MonthMenuObject()

class MonthMenuObject(Node):
    def render(self, context):
        context['blog_months'] = Entry.live.dates("pub_date", "month")
        return ''

def do_get_year_list(parser, token):
    """
    Gets a list of years in which entries are published.
    
    Syntax::
    
    {% get_year_list %}
    """
    return YearMenuObject()

class YearMenuObject(Node):
    def render(self, context):
        context['blog_years'] = Entry.live.dates("pub_date", "year")
        return ''
        
class LatestEntries(template.Node):
  def __init__(self, format_string, var_name):
    self.format_string = format_string
    self.var_name = var_name
  
  def render(self, context):
    posts = Entry.objects.published()[:int(self.format_string)]
    context[self.var_name] = entries
    return ''

def do_get_latest_entries(parser, token):
  """
  Gets any number of latest entries and stores them in a varable.
  
  Syntax::
  
    {% get_latest_entries [limit] as [var_name] %}
  
  Example usage::
    
    {% get_latest_entries 10 as latest_entry_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'(.*?) as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
  format_string, var_name = m.groups()
  return LatestEntries(format_string[0], var_name)


class BlogTags(template.Node):
  def __init__(self, var_name):
    self.var_name = var_name
  
  def render(self, context):
    tags = Tag.objects.all().order_by('title')
    context[self.var_name] = tags
    return ''

def do_get_blog_tags(parser, token):
  """
  Gets all blog tags.
  
  Syntax::
    
    {% get_blog_tags as [var_name] %}
  
  Example usage::
  
    {% get_blog_tags as tag_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
  var_name = m.groups()[0]
  return BlogTags(var_name)

register = template.Library()
register.tag('get_latest_entries', do_get_latest_entries)
register.tag('get_blog_tags', do_get_blog_tags)
register.tag('get_month_list', do_get_month_list)
register.tag('get_year_list', do_get_year_list)