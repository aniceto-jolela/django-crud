from django import template
import os
from django.conf import settings

register = template.Library()


@register.simple_tag
def file_exists(filename):
    is_number = 0
    newfile = filename.replace('/media/profile_pics/', '')
    # Construct the full path to the file
    file_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', newfile)
    if os.path.isfile(file_path):
        is_number = 1
    else:
        is_number = 0

    print(f' Old file =>  {filename}')
    print(f' New file => {newfile}')
    print(f' Is file? => {file_path}')
    # Check if the file exists
    return is_number



