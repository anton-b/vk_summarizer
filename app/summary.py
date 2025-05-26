from app.vk_helpers import VkHelpers
from app.model import summarize_chat, dramatic_chat_summary, describe_image


# 2000000022
def summarize_peer(peer_id, last_messages_num, offset=0):
    vk = VkHelpers()
    history = vk.get_history_with_names(peer_id, last_messages_num, offset)
    link, history_txt = history_to_text(history)
    return link, summarize_chat(history_txt)
    
def summarize_to_povest(peer_id, last_messages_num, offset=0):
    vk = VkHelpers()
    history = vk.get_history_with_names(peer_id, last_messages_num, offset)
    link, history_txt = history_to_text(history)
    return link, dramatic_chat_summary(history_txt)

def get_attachment_photo_url(attachment):
    if attachment["type"] == "photo":
        photo = attachment["photo"]
        for size in photo["sizes"]:
            url = size["url"]
            if size["type"] == "x":
                return size["url"]
        return url

def get_total_photos_in_all_attachments(items):
    total_photos = 0
    for item in items:
        for attachment in item['attachments']:
            if attachment['type'] == 'photo':
                total_photos += 1
    return total_photos

def history_to_text(history):
    link = history[0]['link']
    text = ""
    print(f"Всего фото в этом куске: {get_total_photos_in_all_attachments(history)}\n")                    
    for item in history:
        if item['attachments']:
            for attachment in item['attachments']:
                if attachment['type'] == 'photo':
                    photo_url = get_attachment_photo_url(attachment)
                    print(f"Обнаружено фото в сообщении: {item['date']} от {item['user_name']}\n")
                    print(f"Обработка фото: {photo_url}\n")
                    image_describer = describe_image(photo_url)
                    image_description = ""
                    for img_desc in image_describer.stream({}, stream_mode=['messages']):
                        print(img_desc.content, end='', flush=True)
                        image_description += img_desc.content
                    text += f"({item['date']}) {item['user_name']} добавил фото на котором изображено: ***НАЧАЛО ФОТО*** \n\n{image_description}\n\n ***КОНЕЦ ФОТО***"
        text += f"({item['date']}) {item['user_name']}: {item['text']}\n\n"
    return link, text