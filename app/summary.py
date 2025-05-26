from app.vk_helpers import VkHelpers
from app.model import summarize_chat, dramatic_chat_summary


# 2000000022
def summarize_peer(peer_id, last_messages_num, offset=0):
    vk = VkHelpers()
    history = vk.get_history_with_names(peer_id, last_messages_num, offset)
    history_txt = history_to_text(history)
    return summarize_chat(history_txt)
    
def summarize_to_povest(peer_id, last_messages_num, offset=0):
    vk = VkHelpers()
    history = vk.get_history_with_names(peer_id, last_messages_num, offset)
    history_txt = history_to_text(history)
    return dramatic_chat_summary(history_txt)
    
def history_to_text(history):
    text = ""
    for item in history:
        text += f"({item['date']}) {item['user_name']}: {item['text']}\n\n"
    return text