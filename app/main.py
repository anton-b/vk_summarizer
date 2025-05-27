from app.longpoll import LongPollBot
from app.summary import summarize_peer, summarize_to_povest
from app.auth import Auth
import random

def split_text(summ, max_length=4000):
    """
    Разделяет сводку на части, если она превышает максимальную длину.
    """
    summary = str(summ)
    parts = []
    while len(summary) > max_length:
        part = summary[:max_length]
        last_space = part.rfind(' ')
        if last_space != -1:
            part = part[:last_space]
        parts.append(part)
        summary = summary[len(part):].lstrip()
    if summary:
        parts.append(summary)
    return parts



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
    link, summary, photos = summarize_to_povest(peer_id, last_messages_num=expected_messages, offset=random_offset)    
    
    s = split_text(summary)
    
    for part in s:
        vk_api.messages.send(
            peer_id="2000000066",
            message=f"{part}",
            random_id=0
        )
    rand_photo = random.sample(photos, min(5, len(photos)))  # случайные 2 фото из списка
    for photo in rand_photo:
        vk_api.messages.send(
            peer_id="2000000066",
            attachment=photo,
            message = f"[{photo['url']}|картинка]\n\n{photo['description']}\n\nДата: {photo['date']}\n\n{photo['user_name']}\n\n[{photo['item_link']}|{photo['text'] or 'Оригинал тут'}]",
            random_id=0
        )
    vk_api.messages.send(
            peer_id="2000000066",
            message=f"[{link}|***ссылка на ту часть чатика***]",
            random_id=0
    )