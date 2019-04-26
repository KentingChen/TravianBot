from TravianBot import Travian, logger
import base64
import random
import time
from datetime import datetime
import re


# auto_run_by_min_resource()
tinderbox = Travian("ts2", username, password)
# tinderbox.Village._update_stock()
# print(tinderbox.Village.stock)
last_token = ""
while 1:
    ll = tinderbox.Village.find_token(14)
    token = re.findall("&(c=\w+)(&|$)", ll[0])[0][0]
    if token != last_token:
        last_token = token
        print(datetime.now().strftime("%m-%d %H:%M:%S"))
        print("new token: ", ll)
    time.sleep(random.randint(3, 6))
    ll = tinderbox.Village.find_token(26)
    token = re.findall("&(c=\w+)(&|$)", ll[0])[0][0]
    if token != last_token:
        last_token = token
        print(datetime.now().strftime("%m-%d %H:%M:%S"))
        print("new token: ", ll)
    time.sleep(random.randint(3, 6))
