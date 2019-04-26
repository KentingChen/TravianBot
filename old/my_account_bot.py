#!/usr/bin/env python
from TravianBot import Travian, AlgoRunAs
from pprint import pprint


username = ""
password = ""

gid_queue_dict = {
    "1190": "auto",
    "3144": [10,"auto"] + ["auto"]*10
}


my_account = Travian("ts2", username, password)
AlgoRunAs(my_account).all_build_by_gid(gid_queue_dict)
# AlgoRunAs(my_account).all_auto_by_min_resource()
