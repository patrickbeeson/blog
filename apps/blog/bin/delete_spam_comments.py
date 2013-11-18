import os
import time
import optparse
import datetime

#from django.core.management import setup_environ
#import settings
#setup_environ(settings)

def delete_spam_comments(verbose=False):
    from django.contrib.comments.models import Comment
    spam_comments = Comment.objects.filter(is_public=False)
    deleted_count = spam_comments.count()
    
    for Comment in spam_comments:
    	Comment.delete()
    if spam_comments:
		print "Removed %s spam comments from database" % deleted_count
    
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--settings')
    parser.add_option('-v', '--verbose', action="store_true")
    options, args = parser.parse_args()
    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings
    delete_spam_comments(options.verbose)