from TravianBot import Travian
import base64

username = "your_user_name"
password = "your_password"


def buildup():
    # Put upgrade oid here
    build_oid_queue = []
    
    while 1:
        try:
            my_account = Travian("ts2", your_user_name, your_password)
            while len(build_oid_queue) > 0:
                oid = build_oid_queue[0]
                status = my_account.Village.upgrade(oid)
                if status == "green":
                    done_oid = build_oid_queue.pop(0)
                    logger(f"oid({done_oid}) is building.")
                else:
                    sec = random.randint(150, 180)
                    logger(f"Waiting {sec} seconds.")
                    time.sleep(sec)
            logger("build oid queue is empty now, exit...")
            exit(0)
        except ConnectionError:
            logger("[ERROR] error occurred!")
            time.sleep(random.randint(180, 200))


your_user_name = Travian("ts2", your_user_name, your_password)

your_user_name.Hero.go_adventure()





