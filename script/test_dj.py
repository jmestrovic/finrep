import os
import sys
from django.core.wsgi import get_wsgi_application

# proj_path = 'C:\\work\\projects\\pr\\finrep\\web'
proj_path = '..\\web'
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finrep.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
application = get_wsgi_application()

print("tu sam")
