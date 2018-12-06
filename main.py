from TravianBot import Travian, logger
import base64
import random
import time
from datetime import datetime
import re


username = ""
password = ""
gid_dict = {
                    "1": "伐木場",
                    "2": "泥坑",
                    "3": "鐵礦場",
                    # "4": "農地",
                    "4": "農場",
                    "5": "鋸木廠",
                    "6": "磚廠",
                    "7": "鋼鐵鑄造廠",
                    "8": "麵粉廠",
                    "9": "麵包店",
                    "10": "倉庫",
                    "11": "穀倉",
                    "12": "鐵匠",
                    "13": "盔甲廠",
                    "14": "競技場",
                    "15": "村莊大樓",
                    "16": "集結點",
                    "17": "市場",
                    "18": "大使館",
                    "19": "兵營",
                    "20": "馬廄",
                    "21": "工場",
                    "22": "研究院",
                    "23": "山洞",
                    "24": "城鎮廳",
                    "25": "行宮",
                    "26": "皇宮",
                    "27": "寶物庫",
                    "28": "交易所",
                    "29": "大兵營",
                    "30": "大馬棚",
                    "31": "城牆",
                    "32": "土牆",
                    "33": "木牆",
                    "34": "石匠舖",
                    "35": "釀酒廠",
                    "36": "陷阱",
                    "37": "英雄宅",
                    "38": "大倉庫",
                    "39": "大穀倉",
                    "40": "世界奇觀",
                    "41": "放牧水槽"
                }


def build_by_oid():
    build_oid_queue = [12,13,2,18,5,14,4]
    my_travian_account = Travian("ts2", username, password)
    while 1:
        try:
            while len(build_oid_queue) > 0:
                oid = build_oid_queue[0]
                status = my_travian_account.Village.upgrade(oid)
                if status == "green":
                    done_oid = build_oid_queue.pop(0)
                    logger(f"oid({done_oid}) is building.")
                    sec = random.randint(3, 5)
                    time.sleep(sec)
                else:
                    sec = random.randint(150, 180)
                    logger(f"oid({oid}) skipped. Waiting {sec} seconds.")
                    time.sleep(sec)
            logger("build oid queue is empty now, exit...")
            exit(0)
        except ConnectionError:
            logger("[ERROR] Connection Error occurred!")
            time.sleep(random.randint(180, 200))
            my_travian_account = Travian("ts2", username, password)


def build_by_gid():
    global gid_dict
    gid_queue = [23,23,23,23,23,23]
    my_travian_account = Travian("ts2", username, password)
    while len(gid_queue) > 0:
        last_gid = str(gid_queue[0])
        if int(last_gid) > 4:
            status_dict = my_travian_account.Village.building_status[gid_dict[last_gid]]
            oid = min(status_dict, key=status_dict.get)
        else:
            status_dict = my_travian_account.Village.resource_status[gid_dict[last_gid]]
            oid = min(status_dict, key=status_dict.get)
            if oid == my_travian_account.Village.last_upgrade_oid:
                tmp_dict = dict(status_dict)
                tmp_dict.pop(oid)
                oid = min(tmp_dict, key=tmp_dict.get)
        status = my_travian_account.Village.upgrade(oid)
        if status == "green":
            logger(f"[UPGRADE] : {gid_dict[last_gid]}")
            time.sleep(random.randint(10, 20))
            gid_queue.pop(0)
        else:
            time.sleep(random.randint(160, 180))


def auto_run_by_min_resource():
    my_travian_account = Travian("ts2", username, password)
    adventure_time = time.time()
    while 1:
        try:
            resource_list = my_travian_account.Village.stock
            if resource_list[4] < 15:
                gid = 4  # farm
            else:
                gid = resource_list.index(min(resource_list[0:4])) + 1
            status_dict = my_travian_account.Village.resource_status[gid_dict[str(gid)]]
            oid = min(status_dict, key=status_dict.get)
            if oid == my_travian_account.Village.last_upgrade_oid:
                tmp_dict = dict(status_dict)
                tmp_dict.pop(oid)
                oid = min(tmp_dict, key=tmp_dict.get)
            status = my_travian_account.Village.upgrade(oid)
            if status == "green":
                time.sleep(random.randint(10, 20))
            else:
                time.sleep(random.randint(160, 180))
            if time.time() > adventure_time + 1800:
                my_travian_account.Hero.go_adventure()
                adventure_time = time.time()
        except ConnectionError:
            logger("[ERROR] Connection Error.")
            time.sleep(200)
            my_travian_account = Travian("ts2", username, password)


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
