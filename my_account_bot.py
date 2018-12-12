from TravianBot import Travian, AlgoRunAs
import time

username = ""
password = ""

gid_queue_dict = {
    "1190": [4,17,15,10,11,8,4],
    "3144": [10,11,15,10,11,15]+[4]*15
}


my_acct = Travian("ts2", username, password)
AlgoRunAs(my_acct).all_build_by_gid(gid_queue_dict)
# AlgoRunAs(my_acct).all_auto_by_min_resource()
