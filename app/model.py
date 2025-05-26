from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import mimetypes
import requests
import base64

model = ChatOllama(
    base_url="http://172.29.144.1:11434",
    # model="deepseek-r1:14b",
    # model="phi4:latest",
    model="gemma3:12b",
    # model="llama3.1:8b",
    num_predict=30000,
    # seed=42,
    # temperature=0.01,
)


def system_template(instruction, user_messages):
    return ChatPromptTemplate([("system", instruction)] + user_messages)

def simple_prompt(instruction):
    return PromptTemplate(
        template=instruction,
    )

def blog_bot():
    instruction = """
        Ты полезный и весёлый помошник который превращает историю чата друзей в интересный и увлекательный блог-пост.
        Используй дружелюбный и разговорный тон, чтобы сделать текст лёгким для восприятия.
        Не забывай, что это блог-пост, поэтому старайся сделать его интересным и увлекательным для читателей.
        
        **Твоя задача** написать блог пост по истории чата друзей
        
        **Формат**
        
        - Заголовок.
        - Кто общался в чате, кто они и как их зовут.
        - Введение которое заинтригует читателя и заставляет его продолжить чтение.
        - Основную часть, которая будет содержать интересные моменты из истории чата.        
        - Обязательно укажи участников чата, кто они и как их зовут.
        - Не выделяй оскорбления и негативные моменты.
        - Заключение, которое подведёт итог всему сказанному и оставит читателя с хорошим настроением.

        Вот история беседы:

        ```
        {chat_messages}
        ```
        **Важно** пиши только на русском языке.
        **Важно** Обязательно укажи дату когда происходил чат.
        **Важно** не делай вступлений, типа "Окей вот история чата" или "Вот что я нашёл в чате", просто пиши блог пост.
        **Важно** В заключении определи кто из участников самый выёбистый и дай такому эмодзи медальку 🏅
    """
    return simple_prompt(instruction) | model


def povest_bot():
    instruction = """
**Роль**: Ты — полезный и талантливый литературный помощник, специализирующийся на написании драматических повестей.
**Цель**: На основе переписки друзей ты превращаешь чат в увлекательную, эмоциональную и хорошо структурированную драматическую повесть.
**Стиль**: Используй дружелюбный, живой и разговорный тон, чтобы сделать повесть лёгкой для восприятия и читабельной.
**Атмосфера**: Повесть должна быть драматичной, но не перегруженной трагизмом — добавляй моменты иронии, неловкости, теплоты и близости, как это бывает между друзьями.
**Формат**:

* Преобразуй диалоги в повествование с репликами персонажей.
* Добавляй описания эмоций, пауз, обстановки и действий, чтобы оживить сцены.
* Используй имена персонажей, сохраняя индивидуальность каждого.
* Структурируй повесть по сценам, главам или эпизодам, если материал объёмный.
* Избегай формального или литературно-канцелярского языка — стиль должен быть живым, почти кинематографичным.
* Не забывай упоминать о картинках или фото которое могут быть в чате, если они важны для сюжета.

**Дополнительно**:

* При необходимости придумывай недостающие детали (внешность, локации, внутренние монологи), чтобы усилить сюжет.
* Уважай общий тон переписки — не искажай характеров и намерений участников.

**Вводные данные**: ты получаешь фрагменты чата, на основе которых пишешь повесть.

**Формулировка задачи**: Когда ты получаешь чат друзей, проанализируй его, выдели ключевые конфликты, динамику отношений, скрытые чувства или намёки — и на основе этого создай художественный текст в виде сцены или главы драматической повести.

{chat_messages}
**Важно** пиши только на русском языке.
**Важно** Обязательно укажи дату когда происходил чат.
**Важно** не забывай упоминать о картинках или фото, если они важны для сюжета.
**Важно** не делай вступлений, типа "Окей вот история чата" или "Вот что я нашёл в чате", просто пиши смесь блог поста и повести.
**Важно** В заключении определи кто из участников самый выёбистый и дай такому эмодзи медальку 🏅
**Важно** Начинай всегда так: "А вот и новое случайное воспоминание из чатика от бота-ебобота от <дата>":
    """
    return simple_prompt(instruction) | model
    
def detect_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"  # Default type if detection fails
    return mime_type


def get_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        mime_type = detect_mime_type(url)
        base64_image = base64.b64encode(response.content).decode('utf-8')
        return image_content(base64_image, mime_type)
    else:
        return ""

def image_content(image_data, mime_type=None):
        return {
            "type": "image",
            "source_type": "base64",
            "data": image_data,
            "mime_type": mime_type,
        }

def describe_image(image_url):
    instruction = """
    Ты — полезный и талантливый помощник, специализирующийся на описании изображений.
    Твоя задача — создать подробное и живое описание изображения, которое будет интересно читать.
    Используй дружелюбный и разговорный тон, чтобы сделать текст лёгким для восприятия.
    
    **Формат**:
    - Опиши, что изображено на картинке.
    - Укажи детали, которые могут быть интересны читателю.
    - Используй яркие прилагательные и метафоры, чтобы сделать описание живым.
    - Отдельно извлеки текст и надписи с изображения, если они есть и верни в виде текста. 
    
    **Важно** пиши только на русском языке.
    **Важно** не делай вступлений, типа "Окей вот описание картинки" или "Вот что я вижу на картинке", просто пиши описание.
    """
    image_content = get_image(image_url)
    user_message = {"role": "user", "content":[image_content] }
    return system_template(instruction, [user_message]) | model


def dramatic_chat_summary(chat_messages):
    povest_template = povest_bot()
    input_data = {"chat_messages": chat_messages}
    summary = povest_template.stream(input_data, stream_mode=['messages'])
    summary_a = ""
    for summary_item in summary:
        summary_a += summary_item.content
        print(summary_item.content, end='', flush=True)
    return summary_a


def summarize_chat(chat_messages):
    blog_template = blog_bot()
    input_data = {"chat_messages": chat_messages}
    # summary = blog_template.invoke(input_data)
    summary = blog_template.stream(input_data, stream_mode=['messages'])
    summary_a = ""
    for summary_item in summary:
        summary_a += summary_item.content
        print(summary_item.content, end='', flush=True)
    return summary_a
