class AlgoRunAs:
    def __init__(self, travian_object):
        global gid_dict
        self.TRAVIAN = travian_object

    def _old_all_auto_by_min_resource(self):
        adventure_time = time.time()
        last_oid_dict = {}.fromkeys(self.TRAVIAN.village_newdid_list)
        pprint_two_dicts_not_empty(self.TRAVIAN.Village.resource_status, self.TRAVIAN.Village.building_status)
        while 1:
            try:
                for newdid in self.TRAVIAN.village_newdid_list:
                    self.TRAVIAN.goto(newdid)
                    if len(self.TRAVIAN.Village.resource_status["農場"]) == 15:  # 15 田
                        status_dict = self.TRAVIAN.Village.resource_status[gid_dict[str(4)]]
                        min_food_level = status_dict[min(status_dict, key=status_dict.get)]
                        brick_level = self.TRAVIAN.Village.resource_status["泥坑"]["16"]
                        wood_level = self.TRAVIAN.Village.resource_status["伐木場"]["3"]
                        steel_level = self.TRAVIAN.Village.resource_status["鐵礦場"]["4"]
                        if brick_level < min_food_level - 3:
                            oid = "16"
                            gid = "2"
                        elif wood_level < min_food_level - 3:
                            oid = "3"
                            gid = "1"
                        elif steel_level < min_food_level - 3:
                            oid = "4"
                            gid = "3"
                        else:
                            oid = min(status_dict, key=status_dict.get)
                            gid = "4"
                    else:
                        stock_list = self.TRAVIAN.Village.stock
                        if stock_list[4] < 15:
                            gid = "4"  # farm
                        else:
                            gid = stock_list.index(min(stock_list[0:4])) + 1
                        status_dict = self.TRAVIAN.Village.resource_status[gid_dict[str(gid)]]
                        oid = min(status_dict, key=status_dict.get)
                        if len(status_dict) > 1:
                            if oid == last_oid_dict[newdid]:
                                tmp_dict = dict(status_dict)
                                tmp_dict.pop(oid)
                                oid = min(tmp_dict, key=tmp_dict.get)
                    status = self.TRAVIAN.Village.upgrade(oid)
                    if status == "green":
                        upgrade_item = gid_dict[str(gid)]
                        logger(f"[UPGRADE] : [vid:{newdid}] - {upgrade_item}")
                        last_oid_dict[newdid] = oid
                    time.sleep(random.randint(3, 5))
                time.sleep(random.randint(30, 60))
                if time.time() > adventure_time + random.randint(3600, 4800):
                    self.TRAVIAN.Hero.go_adventure()
                    adventure_time = time.time()
                    time.sleep(random.randint(3, 5))

            except ConnectionError:
                logger("[Error] Connection Error occured.")
            except KeyboardInterrupt:
                logger("[Stop] by Keyboard Interruption.")
                exit(0)

    def _old_build_by_oid(self, build_oid_queue):
        while 1:
            try:
                while len(build_oid_queue) > 0:
                    oid = build_oid_queue[0]
                    status = self.TRAVIAN.Village.upgrade(oid)
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
                self.TRAVIAN = Travian("ts2", username, password)

    def _old_build_by_gid(self, gid_queue):
        while len(gid_queue) > 0:
            last_gid = str(gid_queue[0])
            self.TRAVIAN.update_all_status()
            if int(last_gid) > 4:
                status_dict = self.TRAVIAN.Village.building_status[gid_dict[last_gid]]
                oid = min(status_dict, key=status_dict.get)
            else:
                status_dict = self.TRAVIAN.Village.resource_status[gid_dict[last_gid]]
                oid = min(status_dict, key=status_dict.get)
                if oid == self.TRAVIAN.Village.last_upgrade_oid:
                    tmp_dict = dict(status_dict)
                    tmp_dict.pop(oid)
                    oid = min(tmp_dict, key=tmp_dict.get)
            status = self.TRAVIAN.Village.upgrade(oid)
            if status == "green":
                logger(f"[UPGRADE] : {gid_dict[last_gid]}")
                time.sleep(random.randint(10, 20))
                gid_queue.pop(0)
            else:
                time.sleep(random.randint(160, 180))
        logger("build oid queue is empty now, exit...")
        exit(0)

    def _old_auto_run_by_min_resource(self):
        adventure_time = time.time()
        while 1:
            try:
                self.TRAVIAN.update_all_status()
                stock_list = self.TRAVIAN.Village.stock
                if stock_list[4] < 15:
                    gid = 4  # farm
                else:
                    gid = stock_list.index(min(stock_list[0:4])) + 1
                status_dict = self.TRAVIAN.Village.resource_status[gid_dict[str(gid)]]
                oid = min(status_dict, key=status_dict.get)
                if len(status_dict) > 1:
                    if oid == self.TRAVIAN.Village.last_upgrade_oid:
                        tmp_dict = dict(status_dict)
                        tmp_dict.pop(oid)
                        oid = min(tmp_dict, key=tmp_dict.get)
                status = self.TRAVIAN.Village.upgrade(oid)
                if status == "green":
                    time.sleep(random.randint(10, 20))
                else:
                    time.sleep(random.randint(160, 180))
                if time.time() > adventure_time + 1800:
                    self.TRAVIAN.Hero.go_adventure()
                    adventure_time = time.time()
            except ConnectionError:
                logger("[ERROR] Connection Error.")
                time.sleep(200)