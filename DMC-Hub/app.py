import time
from classes.BotStartupHandler import BotStartupHandler, get_all_sites
from harveyutils.loggerv2 import Logger

logger = Logger(True, "MAIN")

# Base path for sites folders
BASE_PATH = "DMC-Hub/sites"

startup_handler = BotStartupHandler()
site_paths = get_all_sites(BASE_PATH)
logger.msg(f"Loaded [{len(site_paths)}] Sites")

kill_task_data = startup_handler.do_startup(site_paths)

def check_all_tasks_killed():
    all_tasks_killed = False
    while not all_tasks_killed:
        all_tasks_killed = all([data["isKilled"] for data in kill_task_data])
        time.sleep(0.1)

    logger.msg("All tasks killed!")
    # return True

try:
    check_all_tasks_killed()
except KeyboardInterrupt:
    logger.msg(f"Killing tasks")
    for thread in kill_task_data:
        thread["setShouldKill"]()

    check_all_tasks_killed()
