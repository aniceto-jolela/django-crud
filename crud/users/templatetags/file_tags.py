from django import template
from django.conf import settings
import os

register = template.Library()


@register.simple_tag
def file_exists(filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', filename)
    print(file_path)
    # Check if the file exists
    return os.path.isfile(file_path)