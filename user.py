import os
import hashlib
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'mojodemo.settings'

from mojo.models import MojoUser

user = MojoUser(login = sys.argv[1], passwdHash = hashlib.sha256(sys.argv[2]).hexdigest(), mojoToken = sys.argv[3])
user.save()
