import requests
import mechanicalsoup
import base64
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random


def logger(input_object):
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ', end="")
    print(input_object)


class Travian:
    def __init__(self, server, input_name, input_password):
        # pre
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
            self.browser = browser
            self.root_url = root_url
            # data array/dict
            self.alias = {
                "farm": "農場",
                "brick": "泥坑",
                "wood": "伐木場",
                "steel": "鐵礦場"
            }
            self.area_status = {
                "farm": {},
                "brick": {},
                "wood": {},
                "steel": {}
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
            self.gid_dict = {
                # "1": "伐木場",
                # "2": "泥坑",
                # "3": "鐵礦場",
                # "4": "農地",
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

        def print_area(self):
            res = self.browser.open(self.root_url + "dorf1.php")
            area_list = BeautifulSoup(res.content, "html.parser").find_all("area")
            for area in area_list:
                print(area.get("alt"), area.get("href"))

        def update_level_status(self):
            self._update_resource_status()
            self._update_building_status()
            # print(self.area_status)
            # print(self.building_status)

        def _update_resource_status(self):
            url = self.root_url + "dorf1.php"
            res = self.browser.open(url)
            area_list = BeautifulSoup(res.content, "html.parser").find_all("area")
            for area in area_list:
                if "=" in area.get("href"):
                    if self.alias["farm"] == area.get("alt").split()[0]:
                        oid = area.get("href").split("=")[1]
                        level = area.get("alt").split()[2]
                        self.area_status["farm"][oid] = int(level)
                    elif self.alias["brick"] == area.get("alt").split()[0]:
                        oid = area.get("href").split("=")[1]
                        level = area.get("alt").split()[2]
                        self.area_status["brick"][oid] = int(level)
                    elif self.alias["wood"] == area.get("alt").split()[0]:
                        oid = area.get("href").split("=")[1]
                        level = area.get("alt").split()[2]
                        self.area_status["wood"][oid] = int(level)
                    elif self.alias["steel"] == area.get("alt").split()[0]:
                        oid = area.get("href").split("=")[1]
                        level = area.get("alt").split()[2]
                        self.area_status["steel"][oid] = int(level)

        def _update_building_status(self):
            url = self.root_url + "dorf2.php"
            res = self.browser.open(url)
            village_map = BeautifulSoup(res.content, "html.parser").find(id="village_map")
            building_slot_list = BeautifulSoup(str(village_map), "html.parser").find_all("div")
            level_watcher = False
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
                if level_watcher:
                    if slot_item_list[0] == "labelLayer":
                        level = slot.string
                        self.building_status[self.gid_dict[gid]][oid] = int(level)

        def upgrade(self, oid):
            url = f"https://ts2.travian.tw/build.php?id={oid}"
            res = self.browser.open(url)
            button_list = BeautifulSoup(res.content, "html.parser").find_all("button")
            for button in button_list:
                # "green build" means it can be upgraded.
                if {"green", "build"} == set(button.get("class")):
                    url_list_found = re.findall(r"'(\S*)'", button.get("onclick"))
                    if len(url_list_found) == 1:
                        postfix = url_list_found[0]
                        self.browser.get(self.root_url + postfix)
                        logger(f"call upgrade oid[{oid}] success")
                        return "green"  # upgraded success.
                    else:
                        logger("[ERROR] Multiple url list found! : "+ str(url_list))
                # "gold builder" means not yet or resources insufficient.
                elif {"gold", "builder"} == set(button.get("class")):
                    return "gold"

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
            # print(adventure_list)
            if len(adventure_list) > 0:
                self.browser.open(self.root_url + f"start_adventure.php?from=list&kid={adventure_list[0]}")
                try:
                    self.browser.select_form("form[action=/start_adventure.php]")
                    self.browser.submit_selected()
                    return "success"
                except mechanicalsoup.utils.LinkNotFoundError:
                    logger("Hero is not in Village.")
                    return "unavailable"

