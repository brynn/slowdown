#!/usr/bin/python2.7

import urllib2, os, datetime
from dateutil import tz
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')
utc = datetime.datetime.now()
utc = utc.replace(tzinfo=from_zone)
est = utc.astimezone(to_zone)

f = open(os.path.join(BASE_DIR, 'logging.txt'), 'a')
f.write(str(est) + '\n')
response = urllib2.urlopen("http://slowdown.io/check-and-send-email?secret=vQbJbBwjQLkB").read()
f.write(response + '\n\n')
f.close()