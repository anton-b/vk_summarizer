from app.longpoll import LongPollBot
from app.summary import summarize_peer, summarize_to_povest
from app.auth import Auth
import random
if __name__ == "__main__":
    """
    Запуск бота
    """
    # bot = LongPollBot()
    # bot.run_long_poll()
    
    vk_auth = Auth()
    vk_api = vk_auth.vk_api
    peer_id = 2000000022  # ID чата, для которого будет работать бот
    total_messages = 450000
    
    random_offset = random.randint(0, total_messages - 200)  # случайный оффсет для получения сообщений
    print(f"Используем оффсет: {random_offset}")
    
    expected_messages = 600  # ожидаемое количество сообщений для сводки
    message_count = 0  # счётчик сообщений
    # summary = summarize_peer(peer_id, last_messages_num=expected_messages, offset=50000)
    link, summary = summarize_to_povest(peer_id, last_messages_num=expected_messages, offset=random_offset)
    vk_api.messages.send(
    peer_id="2000000066",
    message=f"{summary}\n\n [{link}|ссылка на начало]",
    random_id=0
    )