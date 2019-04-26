import mechanicalsoup
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import pprint


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


def pprint_two_dicts_not_empty(d1, d2):
    not_empty_d2 = {k: v for k, v in d2.items() if bool(v) is True}
    d1.update(not_empty_d2)
    pprint.pprint(d1)


def update_upgraded_item_count(upgraded_dict, upgraded_item):
    global gid_dict
    if upgraded_item not in upgraded_dict:
        upgraded_dict[upgraded_item] = 1
    else:
        upgraded_dict[upgraded_item] += 1
    return upgraded_dict


class Travian:
    def __init__(self, server, input_name, input_password):
        # init
        global gid_dict
        self.server = server
        self.root_url = f"https://{self.server}.travian.com/"
        self.username = input_name
        self.password = input_password
        self.browser = mechanicalsoup.StatefulBrowser(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 ("
                       "KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        )
        self.current_newdid = ""
        self.village_newdid_list = []

        # class
        self._login()
        self._fetch_all_villa_list()
        pprint.pprint(self.village_newdid_list)
        self.Village = None  # self._Village(self.browser, self.root_url)
        self.goto(self.village_newdid_list[0])
        self.Hero = self.Hero(browser=self.browser, root_url=self.root_url)

    def _login(self):
        self.browser.open(self.root_url)
        self.browser.select_form("form[action=dorf1.php]")
        self.browser["name"] = self.username
        self.browser["password"] = self.password
        self.browser.submit_selected()

    def _fetch_all_villa_list(self):
        url = self.root_url + "dorf1.php"
        res = self.browser.open(url)
        html_village_list = BeautifulSoup(res.content, "html.parser").find(id="sidebarBoxVillagelist")
        li_list = BeautifulSoup(str(html_village_list), "html.parser").find_all("a")
        for a in li_list:
            newdid = a.get("href").split("=")[1].replace("&", "")
            self.village_newdid_list.append(newdid)

    def goto(self, newdid):
        newdid = str(newdid)
        newdid_link = self.root_url + f"dorf1.php?newdid={newdid}&"
        self.current_newdid = newdid
        self.browser.open(newdid_link)
        self.Village = self._Village(self.browser, self.root_url)
        # self.Village.update_all_status()

    class _Village:
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
            # self._update_stock()
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
            # resouce
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
            # stock
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
            # stock
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

        def upgrade(self, oid):
            oid = str(oid)
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
                return "blank_list"


class AlgoRunAs:
    def __init__(self, travian_object):
        global gid_dict
        self.TRAVIAN = travian_object

    def all_build_by_gid(self, gid_queue_dict):
        report_time = time.time()
        adventure_time = time.time()
        last_oid_dict = {}.fromkeys(self.TRAVIAN.village_newdid_list)
        upgraded_item_dict = {}
        pprint.pprint(gid_queue_dict)
        while any(l for l in gid_queue_dict.values()):
            try:
                for newdid in self.TRAVIAN.village_newdid_list:
                    if newdid in gid_queue_dict and bool(gid_queue_dict[newdid]) is True:
                        self.TRAVIAN.goto(newdid)
                        # if use auto (upgrade by min stock)
                        if gid_queue_dict[newdid] == "auto" or gid_queue_dict[newdid][0] == "auto":
                            if len(self.TRAVIAN.Village.resource_status["農場"]) == 15:  # 15 田
                                status_dict = self.TRAVIAN.Village.resource_status[gid_dict[str(4)]]
                                min_food_level = status_dict[min(status_dict, key=status_dict.get)]
                                brick_level = self.TRAVIAN.Village.resource_status["泥坑"]["16"]
                                wood_level = self.TRAVIAN.Village.resource_status["伐木場"]["3"]
                                steel_level = self.TRAVIAN.Village.resource_status["鐵礦場"]["4"]
                                if brick_level < min_food_level - 3:
                                    oid = "16"
                                    last_gid = "2"
                                elif wood_level < min_food_level - 3:
                                    oid = "3"
                                    last_gid = "1"
                                elif steel_level < min_food_level - 3:
                                    oid = "4"
                                    last_gid = "3"
                                else:
                                    last_gid = "4"
                                    status_dict = self.TRAVIAN.Village.resource_status[gid_dict[str(last_gid)]]
                                    oid = min(status_dict, key=status_dict.get)
                                    if len(status_dict) > 1:
                                        if oid == last_oid_dict[newdid]:
                                            tmp_dict = dict(status_dict)
                                            tmp_dict.pop(oid)
                                            oid = min(tmp_dict, key=tmp_dict.get)
                            else:  # not 15 田
                                stock_list = self.TRAVIAN.Village.stock
                                if stock_list[4] < 15:  # danger food balance
                                    last_gid = "4"  # farm
                                else:
                                    last_gid = str(stock_list.index(min(stock_list[0:4])) + 1)
                                status_dict = self.TRAVIAN.Village.resource_status[gid_dict[str(last_gid)]]
                                oid = min(status_dict, key=status_dict.get)
                                if len(status_dict) > 1:
                                    if oid == last_oid_dict[newdid]:
                                        tmp_dict = dict(status_dict)
                                        tmp_dict.pop(oid)
                                        oid = min(tmp_dict, key=tmp_dict.get)
                        # if use gid
                        else:
                            last_gid = str(gid_queue_dict[newdid][0])
                            if int(last_gid) > 4:
                                status_dict = self.TRAVIAN.Village.building_status[gid_dict[last_gid]]
                                oid = min(status_dict, key=status_dict.get)
                            else:
                                status_dict = self.TRAVIAN.Village.resource_status[gid_dict[last_gid]]
                                oid = min(status_dict, key=status_dict.get)
                                if oid == last_oid_dict[newdid]:
                                    tmp_dict = dict(status_dict)
                                    tmp_dict.pop(oid)
                                    oid = min(tmp_dict, key=tmp_dict.get)
                        status = self.TRAVIAN.Village.upgrade(oid)
                        if status == "green":
                            upgraded_item = gid_dict[str(last_gid)]
                            logger(f"[UPGRADE] : [vid:{newdid}] - {upgraded_item}")
                            last_oid_dict[newdid] = oid
                            upgraded_item_dict = update_upgraded_item_count(upgraded_item_dict, upgraded_item)
                            if type(gid_queue_dict[newdid]) == list:
                                gid_queue_dict[newdid].pop(0)
                            if any(set(v) != set("auto") for v in gid_queue_dict.values()):
                                pprint.pprint(gid_queue_dict)
                    time.sleep(random.randint(3, 5))
                time.sleep(random.randint(200, 300))
                if time.time() > adventure_time + random.randint(3600, 4800):
                    self.TRAVIAN.Hero.go_adventure()
                    adventure_time = time.time()
                    time.sleep(random.randint(3, 5))
                if time.time() > report_time + 36000:
                    print("\n - Upgraded item list in the Last Run:")
                    pprint.pprint(upgraded_item_dict)
                    report_time = time.time()
            except ConnectionError as error_message:
                logger("[Error] Connection Error occured.")
                logger(f"[ErrorMessage] {error_message}")
            except KeyboardInterrupt:
                logger("[Stop] by Keyboard Interruption.")
                raise KeyboardInterrupt
            except TypeError as error_message:
                logger("[Error] Type Error!")
                logger(f"[ErrorMessage] {error_message}")
            except ValueError as error_message:
                logger("[Error] Value Error!")
                logger(f"[ErrorMessage] {error_message}")
            except Exception as error_message:
                logger(" ! [UNHANDLED ERROR] !")
                logger(f"[ErrorMessage] {error_message}")
                print("\n - Upgraded item list in the Last Run:")
                pprint.pprint(upgraded_item_dict)
                exit(0)
        logger("[DONE] All queues are empty.")


