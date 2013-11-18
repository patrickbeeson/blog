from django.db.models import Manager
import datetime


class ManagerWithPublished(Manager):
  """ Same as above but for more for templates """
  def published(self):
    return self.get_query_set().filter(status__gte=3, pub_date__lte=datetime.datetime.now())