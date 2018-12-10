from TravianBot import Travian, AlgoRunAs
import base64

username = "my_username"
password = "password"

my_account = Travian("ts2", username, password)
# AlgoRunAs(my_account).build_by_oid([1,3,7,11,26])
# AlgoRunAs(my_account).build_by_gid([1,2,3,4,15,15])
AlgoRunAs(my_account).auto_run_by_min_resource()


