import os
import hashlib
import sys
from tools import instamojo

os.environ['DJANGO_SETTINGS_MODULE'] = 'mojodemo.settings'

from mojo.models import MojoUser
api = instamojo.API()
api.auth(sys.argv[1],sys.argv[2])
token = api.token

user = MojoUser(login = sys.argv[1], passwdHash = hashlib.sha256(sys.argv[2]).hexdigest(), mojoToken = token)
user.save()
