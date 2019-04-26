from TravianBot import Travian, AlgoRunAs
import base64
from pprint import pprint
import time

username = "黃博老司機"
password = "gooddriverhuang"

gid_queue_dict = {
    #"3842": "auto"
    "3842": [25]
}

while any(l for l in gid_queue_dict.values()):
    try:
        tinderbox = Travian("ts3.chinese", username, password)
        AlgoRunAs(tinderbox).all_build_by_gid(gid_queue_dict)
    # AlgoRunAs(tinderbox).all_auto_by_min_resource()
    except KeyboardInterrupt:
        exit(0)
    except:
        time.sleep(1800)

