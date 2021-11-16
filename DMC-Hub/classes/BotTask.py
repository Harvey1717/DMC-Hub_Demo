import base64
import json
from threading import Lock
from classes.Task import Task, tasks_decorator
from selenium import webdriver


class BotTask(Task):
    """The child class of a Task class,
    used for monitors.

    Arguements:
        thread_lock: A lock shared between all tasks.

        kill_task_list: A list of dict data containing Task.kill_task_data.

        task_number: Task (thread) number.
        settings: JSON from settings/settings.json and settings_dev.json.
        task_data: Data from a task file.
        profile_data: A profile from the profiles file.

    Attributes:
        kill_task_data: A requests session.
        thread_lock: A requests session.
        task_number: A requests session.
        settings: A requests session.
        task_data: A requests session.
        profile_data: A requests session.
        ses: A requests session.
        logger: A logger object.
    """

    def __init__(
        self,
        thread_lock: Lock,
        kill_task_list: list,
        task_number: int,
        settings: dict,
        task_data: dict,
        profile_data: dict,
    ) -> None:
        super().__init__(
            thread_lock, kill_task_list, task_number, settings, task_data, profile_data
        )

    @tasks_decorator
    def get_driver(self):
        driver = webdriver.Chrome("./chromedriver")
        return driver

    @tasks_decorator
    def open_browser(self, driver, html=None, url=None):
        self.logger.alert("OPENING BROWSER, CODE EXECUTION WILL BLOCK")

        cookies_to_set = []
        for c in self.ses.cookies:
            cookies_to_set.append(
                # {"name": c.name, "value": c.value, "domain": c.domain}
                {"name": c.name, "value": c.value}
            )
        for cookie in cookies_to_set:
            driver.add_cookie(cookie)

        if html:
            html_bs64 = base64.b64encode(html.encode("utf-8")).decode()
            driver.get("data:text/html;base64," + html_bs64)
        elif url:
            driver.get(url)

        while True:
            self.sleep_custom(5000, should_log=False)

    @tasks_decorator
    def encode_url(self, url: str) -> str:
        BASE_URL = "dmc.hub"  # If changed extension needs changing too

        url_bytes = url.encode("ascii")
        url_bytes_encoded = base64.b64encode(url_bytes)
        url_encoded = url_bytes_encoded.decode("ascii")

        cookies = []
        for c in self.ses.cookies:
            if not (c.domain.startswith("www.") or c.domain.startswith("https")):
                url = f"https://{c.domain}"

            if c.domain.startswith("."):
                url = f"www{c.domain}"

            cookies.append(
                {"name": c.name, "value": c.value, "domain": c.domain, "url": url}
            )

        print("All cookies below")
        print(cookies)

        cookie_json_string = json.dumps(cookies)
        cookie_json_string_bytes = cookie_json_string.encode("ascii")
        cookie_json_string_bytes_encoded = base64.b64encode(cookie_json_string_bytes)
        cookie_json_string_encoded = cookie_json_string_bytes_encoded.decode("ascii")

        return f"https://{BASE_URL}/setCookies?redirectURL={url_encoded}&cookies={cookie_json_string_encoded}&mainDomain=redacted.org&checkIsAdded=true"
