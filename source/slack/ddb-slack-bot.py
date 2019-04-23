import logging
import time
from slackclient import SlackClient
logging.basicConfig()

sc = SlackClient(token)

print (sc.api_call("users.list") )

if sc.rtm_connect():
    while True:
            print sc.rtm_read()
            time.sleep(1)
else:
    print "Connection Failed"

