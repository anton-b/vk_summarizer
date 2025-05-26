from app.vk_helpers import VkHelpers
from app.model import summarize_chat, dramatic_chat_summary


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
    
def history_to_text(history):
    link = history[0]['link']
    text = ""
    for item in history:
        text += f"({item['date']}) {item['user_name']}: {item['text']}\n\n"
    return link, text