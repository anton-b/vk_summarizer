from vk_api import VkApi
from app.config import TOKEN

class Auth:

    def __init__(self):
        self.vk_session = None
        self.vk_api = None
        self.do_auth()
    
    def do_auth(self):
        token = TOKEN
        try:
            self.vk_session = VkApi(token=token)
            self.vk_api = self.vk_session.get_api()
            return self.vk_api
        except Exception as error:
            print(error)
            return None
