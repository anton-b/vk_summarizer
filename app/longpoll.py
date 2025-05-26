from vk_api.longpoll import (
    VkLongPoll,
    VkEventType,
)  # использование VkLongPoll и VkEventType
from app.auth import Auth
import json  # для работы с json
from app.summary import summarize_peer  # импорт функции summarize_peer из summary.py


class LongPollBot:

    # длительное подключение
    long_poll = None

    def __init__(self):
        self.auth = Auth()  # авторизация
        self.vk_session = self.auth.vk_session
        self.vk_api = self.auth.vk_api
        self.long_poll = VkLongPoll(self.vk_session, mode=8)  # инициализация long poll
        self.history = [] # инициализация истории сообщений
        self.peer_id = 2000000022  # ID чата, для которого будет работать бот
 # инициализация помощника для работы с VK API
    
    def save_history(self, history):
        with open("history.json", "w", encoding='utf-8') as file:
            h = json.dumps(history, ensure_ascii=False)
            file.write(h)
            
    def run_long_poll(self):
        expected_messages = 200  # ожидаемое количество сообщений для сводки
        message_count = 0  # счётчик сообщений
        summary = summarize_peer(self.peer_id, last_messages_num=expected_messages, offset=0)
        print(f"Сводка для последних {expected_messages} сообщений: {summary}")
        self.vk_api.messages.send(
            peer_id=self.peer_id,
            message=f"{summary}",
            random_id=0
        )
        for event in self.long_poll.listen():
            # print(event.raw)
            if event.type == VkEventType.MESSAGE_NEW:
               if event.peer_id == 2000000022:  # проверяем, что сообщение из нужного чата
                print(f"Новое сообщение в чате {event.peer_id}: {event.text}")
                message_count += 1  # увеличиваем счётчик сообщений
                print("До саммари осталось сообщений:", expected_messages - message_count % expected_messages)
                if message_count % expected_messages == 0:
                    summary = summarize_peer(event.peer_id, last_messages_num=300, offset=0)
                    print(f"Сводка для последних 300 сообщений: {summary}")
                    self.vk_api.messages.send(
                        peer_id=event.peer_id,
                        message=f"{summary}",
                        random_id=0
                    )
                       
            
            
            # если пришло новое сообщение - происходит проверка текста сообщения
            # if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                # print(f"Новое сообщение: {event.text}")
            #     print(f"Новое сообщение: {event.chat_id}")
            #     print(f"Новое сообщение: {event.user_id}")

            #     # если была получена одна из заданных фраз
            #     if event.text == "Привет" or event.text == "Здравствуй":

            #         # ответ отправляется в личные сообщения пользователя (если сообщение из личного чата)
            #         if event.from_user:
            #             self.send_message(
            #                 receiver_user_id=event.user_id, message_text="И тебе привет"
            #             )

            #         # ответ отпрвляется в беседу (если сообщение было получено в общем чате)
            #         elif event.from_chat:
            #             self.send_message(
            #                 receiver_user_id=event.chat_id, message_text="Всем привет"
            #             )
