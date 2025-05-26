from app.auth import Auth
from functools import lru_cache


class VkHelpers:
    def __init__(self):
        self.auth = Auth()
        self.vk_api = self.auth.vk_api

    def date_from_ts_to_str(self, ts):
        from datetime import datetime

        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    def get_history_with_names(self, peer_id, last_messages_num=200, offset=0):
        vk_api = self.vk_api
        hist = []
        if last_messages_num > 200:
            for i in range(0, last_messages_num, 200):
                history_part = vk_api.messages.get_history(
                    peer_id=peer_id, extended=1, count=200, offset=offset + i
                )
                print(f"Получено {len(history_part['items'])} сообщений с оффсетом {i}")
                hist.extend(history_part["items"])
        else:
            hist = vk_api.messages.get_history(
                peer_id=peer_id, extended=1, count=last_messages_num, offset=offset
            )  # Reverse to have the oldest messages first
            hist = hist["items"]
        return self.history_to_history_item(hist)

    def history_to_history_item(self, history):
        history_items = []
        for item in reversed(history):
            if "text" in item:
                user_name = self.get_user(item["from_id"])
                history_items.append(
                    {
                        "user_name": user_name,
                        "text": item["text"],
                        "date": self.date_from_ts_to_str(item["date"]),
                    }
                )
        return history_items

    @lru_cache(maxsize=1000)
    def get_user(self, user_id):
        vk_api = self.vk_api
        user_info = vk_api.users.get(user_ids=user_id, fields="first_name,last_name")
        if user_info:
            return f"{user_info[0]['first_name']} {user_info[0]['last_name']}"
        return "Unknown User"
