import requests
from datetime import datetime

# TODO re comment


def send_hook(webhook, content):
    json_data = {
        "content": f"{content}",
    }
    res = requests.post(webhook, json=json_data)
    if res.status_code != 204:
        return f"Webhook not sent. Got response {res.status_code}"
    else:
        return f"Webhook sent with response code {res.status_code}"


class Embed:
    def __init__(self):
        self.embed = {}

    def set_title(self, title):
        self.embed["title"] = f"{title}"

    def set_description(self, description):
        self.embed["description"] = f"{description}"

    def set_colour(self, colour):
        self.embed["color"] = f"{int(colour, 16)}"

    def set_url(self, url):
        self.embed["url"] = f"{url}"

    def add_field(self, field_name, field_value, inline=False):
        if "fields" in self.embed.keys():
            self.embed["fields"].append(
                {"name": f"{field_name}", "value": f"{field_value}", "inline": inline}
            )
        else:
            self.embed["fields"] = [
                {"name": f"{field_name}", "value": f"{field_value}", "inline": inline}
            ]

    def set_footer(self, footer_text):
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S:%f")
        self.embed["footer"] = {"text": f"{footer_text} - {ts}"}

    def set_timestamp(self):
        date = datetime.now()
        # Currently not working in Discord
        # self.embed["timestamp"] = datetime.now().isoformat()
        # date = datetime.now()
        # ms = date.strftime("%f")[:3]
        # print(date.strftime(f"%Y-%m-%dT%H:%M:%S.{ms}Z"))
        # self.embed["timestamp"] = date.strftime(f"%Y-%m-%dT%H:%M:%S.{ms}Z")

        # TEMP SOLUTION IN SET_FOOTER

    def set_thumbnail(self, img_url):
        self.embed["thumbnail"] = {"url": img_url}

    def send(self, webhook, username="", content="", avatar_url=""):
        json_data = {
            "embeds": [self.embed],
            "username": f"{username}",
            "content": f"{content}",
            "avatar_url": avatar_url,
        }
        res = requests.post(webhook, json=json_data)
        if res.status_code != 204:
            return f"Webhook not sent. Got response {res.status_code}"
        else:
            return f"Webhook sent with response code {res.status_code}"
