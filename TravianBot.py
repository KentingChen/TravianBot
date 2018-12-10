import mechanicalsoup
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random


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


def logger(input_object):
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ', end="")
    print(input_object)


class Travian:
    def __init__(self, server, input_name, input_password):
        # init
        global gid_dict
        self.server = server
        self.root_url = f"https://{self.server}.travian.tw/"
        self.username = input_name
        self.password = input_password
        self.browser = mechanicalsoup.StatefulBrowser(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 ("
                       "KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        )

        # class
        self.login()
        self.Village = self.Village(browser=self.browser, root_url=self.root_url)
        self.Hero = self.Hero(browser=self.browser, root_url=self.root_url)

    def login(self):
        self.browser.open(self.root_url)
        self.browser.select_form("form[action=dorf1.php]")
        self.browser["name"] = self.username
        self.browser["password"] = self.password
        self.browser.submit_selected()

    class Village:
        def __init__(self, browser, root_url):
            # init
            self.browser = browser
            self.root_url = root_url
            # static dict
            self.alias = {
                "farm": "農場",
                "brick": "泥坑",
                "wood": "伐木場",
                "steel": "鐵礦場"
            }
            # Dynamic dict (data)
            self.last_upgrade_oid = ""
            self.stock = [0, 0, 0, 0, 0]
            self.resource_status = {
                "農場": {},
                "泥坑": {},
                "伐木場": {},
                "鐵礦場": {}
            }
            self.building_status = {
                "blank": [],
                # "伐木場": {},
                # "泥坑": {},
                # "鐵礦場": {},
                # "農地": {},
                "鋸木廠": {},
                "磚廠": {},
                "鋼鐵鑄造廠": {},
                "麵粉廠": {},
                "麵包店": {},
                "倉庫": {},
                "穀倉": {},
                "鐵匠": {},
                "盔甲廠": {},
                "競技場": {},
                "村莊大樓": {},
                "集結點": {},
                "市場": {},
                "大使館": {},
                "兵營": {},
                "馬廄": {},
                "工場": {},
                "研究院": {},
                "山洞": {},
                "城鎮廳": {},
                "行宮": {},
                "皇宮": {},
                "寶物庫": {},
                "交易所": {},
                "大兵營": {},
                "大馬棚": {},
                "城牆": {},
                "土牆": {},
                "木牆": {},
                "石匠舖": {},
                "釀酒廠": {},
                "陷阱": {},
                "英雄宅": {},
                "大倉庫": {},
                "大穀倉": {},
                "世界奇觀": {},
                "放牧水槽": {}
            }
            # method
            self.update_all_status()

        def update_all_status(self):
            self._update_resource_level()
            self._update_stock()
            self._update_building_level()

        def _update_stock(self):
            url = self.root_url + "dorf1.php"
            res = self.browser.open(url)
            wood_stock = BeautifulSoup(res.content, "html.parser").find("span", id="l1").string
            brick_stock = BeautifulSoup(res.content, "html.parser").find("span", id="l2").string
            steel_stock = BeautifulSoup(res.content, "html.parser").find("span", id="l3").string
            food_stock = BeautifulSoup(res.content, "html.parser").find("span", id="l4").string
            food_balance = BeautifulSoup(res.content, "html.parser").find("span", id="stockBarFreeCrop").string
            self.stock[0] = int(str(wood_stock).strip().replace(",", "").lstrip("\u202d").rstrip("\u202c"))
            self.stock[1] = int(str(brick_stock).strip().replace(",", "").lstrip("\u202d").rstrip("\u202c"))
            self.stock[2] = int(str(steel_stock).strip().replace(",", "").lstrip("\u202d").rstrip("\u202c"))
            self.stock[3] = int(str(food_stock).strip().replace(",", "").lstrip("\u202d").rstrip("\u202c"))
            self.stock[4] = int(str(food_balance).strip().replace(",", "").lstrip("\u202d").rstrip("\u202c"))

        def _update_resource_level(self):
            url = self.root_url + "dorf1.php"
            res = self.browser.open(url)
            area_list = BeautifulSoup(res.content, "html.parser").find_all("area")
            for area in area_list:
                if "=" in area.get("href"):
                    if "農場" == area.get("alt").split()[0]:
                        oid = area.get("href").split("=")[1]
                        level = area.get("alt").split()[2]
                        self.resource_status["農場"][oid] = int(level)
                    elif "泥坑" == area.get("alt").split()[0]:
                        oid = area.get("href").split("=")[1]
                        level = area.get("alt").split()[2]
                        self.resource_status["泥坑"][oid] = int(level)
                    elif "伐木場" == area.get("alt").split()[0]:
                        oid = area.get("href").split("=")[1]
                        level = area.get("alt").split()[2]
                        self.resource_status["伐木場"][oid] = int(level)
                    elif "鐵礦場" == area.get("alt").split()[0]:
                        oid = area.get("href").split("=")[1]
                        level = area.get("alt").split()[2]
                        self.resource_status["鐵礦場"][oid] = int(level)
            logger("[core] updating resource status is done.")

        def _update_building_level(self):
            url = self.root_url + "dorf2.php"
            res = self.browser.open(url)
            village_map = BeautifulSoup(res.content, "html.parser").find(id="village_map")
            building_slot_list = BeautifulSoup(str(village_map), "html.parser").find_all("div")
            level_watcher = False
            gid = 0
            oid = 0
            for slot in building_slot_list:
                slot_item_list = slot.get("class")
                if len(slot_item_list) > 2:
                    # print(slot_item_list)
                    if slot_item_list[0] == "buildingSlot" and slot_item_list[2].startswith("g"):
                        oid = slot_item_list[1].replace("a", "")
                        gid = slot_item_list[2].replace("g", "")
                        if gid != "0":  # building exists
                            level_watcher = True
                        elif gid == "0":  # blank area
                            level_watcher = False
                            self.building_status["blank"].append(oid)
                if level_watcher is True:
                    if slot_item_list[0] == "labelLayer":
                        level = slot.string
                        self.building_status[gid_dict[gid]][oid] = int(level)
                        level_watcher = False
            logger("[core] updating building status is done.")

        def upgrade(self, oid):
            url = self.root_url + f"build.php?id={oid}"
            res = self.browser.open(url)
            button_list = BeautifulSoup(res.content, "html.parser").find_all("button")
            for button in button_list:
                # "green build" means it can be upgraded.
                if {"green", "build"} == set(button.get("class")):
                    url_list_found = re.findall(r"'(\S*)'", button.get("onclick"))
                    if len(url_list_found) == 1:
                        postfix = url_list_found[0]
                        self.browser.get(self.root_url + postfix)
                        logger(f"[VILLAGE] call upgrade oid[{oid}] success")
                        self.last_upgrade_oid = oid
                        self.update_all_status()
                        return "green"  # upgraded success.
                    else:
                        logger("[ERROR] Multiple url list found! : " + str(url_list))
                # "gold builder" means not yet or resources insufficient.
                elif {"gold", "builder"} == set(button.get("class")):
                    return "gold"

        def _tmp_find_token(self, oid):
            url = self.root_url + f"build.php?id={oid}"
            res = self.browser.open(url)
            button_list = BeautifulSoup(res.content, "html.parser").find_all("button")
            for button in button_list:
                if {"green", "build"} == set(button.get("class")):
                    url_list_found = re.findall(r"'(\S*)'", button.get("onclick"))
                    return url_list_found
                elif {"gold", "builder"} == set(button.get("class")):
                    url_list_found = re.findall(r"'(\S*)'", button.get("onclick"))
                    return url_list_found

        def get_building_queue_timer(self):
            timer_list = []
            url = self.root_url + "dorf1.php"
            res = self.browser.open(url)
            span_list = BeautifulSoup(res.content, "html.parser").find_all("span")
            for span in span_list:
                if span.parent.get("class")[0] == "buildDuration":
                    timer_list.append(int(span.get("value")))
            return timer_list

    class Hero:
        def __init__(self, browser, root_url):
            self.browser = browser
            self.root_url = root_url

        def go_adventure(self):
            adventure_list = []
            url = self.root_url + "hero.php?t=3"
            res = self.browser.open(url)
            tr_list = BeautifulSoup(res.content, "html.parser").find_all("tr")
            for tr in tr_list:
                tr_string = str(tr.get("id"))
                if "adventure" in tr_string:
                    adventure_list.append(tr_string.replace("adventure", ""))
            if len(adventure_list) > 0:
                self.browser.open(self.root_url + f"start_adventure.php?from=list&kid={adventure_list[0]}")
                try:
                    self.browser.select_form("form[action=/start_adventure.php]")
                    self.browser.submit_selected()
                    logger("[Hero] Go Adventure.")
                    return "success"
                except mechanicalsoup.utils.LinkNotFoundError:
                    logger("[Hero] Hero is not in Village.")
                    return "unavailable"
            else:
                # logger("[Hero] No adventure available.")
                return "blank_list"


class AlgoRunAs:
    def __init__(self, travian_object):
        global gid_dict
        self.my_travian_account = travian_object

    def build_by_oid(self, build_oid_queue):
        while 1:
            try:
                while len(build_oid_queue) > 0:
                    oid = build_oid_queue[0]
                    status = self.my_travian_account.Village.upgrade(oid)
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
                self.my_travian_account = Travian("ts2", username, password)

    def build_by_gid(self, gid_queue):
        while len(gid_queue) > 0:
            last_gid = str(gid_queue[0])
            if int(last_gid) > 4:
                status_dict = self.my_travian_account.Village.building_status[gid_dict[last_gid]]
                oid = min(status_dict, key=status_dict.get)
            else:
                status_dict = self.my_travian_account.Village.resource_status[gid_dict[last_gid]]
                oid = min(status_dict, key=status_dict.get)
                if oid == self.my_travian_account.Village.last_upgrade_oid:
                    tmp_dict = dict(status_dict)
                    tmp_dict.pop(oid)
                    oid = min(tmp_dict, key=tmp_dict.get)
            status = self.my_travian_account.Village.upgrade(oid)
            if status == "green":
                logger(f"[UPGRADE] : {gid_dict[last_gid]}")
                time.sleep(random.randint(10, 20))
                gid_queue.pop(0)
            else:
                time.sleep(random.randint(160, 180))
        logger("build oid queue is empty now, exit...")
        exit(0)

    def auto_run_by_min_resource(self):
        adventure_time = time.time()
        while 1:
            try:
                resource_list = self.my_travian_account.Village.stock
                if resource_list[4] < 15:
                    gid = 4  # farm
                else:
                    gid = resource_list.index(min(resource_list[0:4])) + 1
                status_dict = self.my_travian_account.Village.resource_status[gid_dict[str(gid)]]
                oid = min(status_dict, key=status_dict.get)
                if len(status_dict) > 1:
                    if oid == self.my_travian_account.Village.last_upgrade_oid:
                        tmp_dict = dict(status_dict)
                        tmp_dict.pop(oid)
                        oid = min(tmp_dict, key=tmp_dict.get)
                status = self.my_travian_account.Village.upgrade(oid)
                if status == "green":
                    time.sleep(random.randint(10, 20))
                else:
                    time.sleep(random.randint(160, 180))
                if time.time() > adventure_time + 1800:
                    self.my_travian_account.Hero.go_adventure()
                    adventure_time = time.time()
            except ConnectionError:
                logger("[ERROR] Connection Error.")
                time.sleep(200)
                self.my_travian_account = Travian("ts2", username, password)
