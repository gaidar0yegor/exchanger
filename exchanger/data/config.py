import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Get environment variables or use defaults
BOT_TOKEN = os.getenv('BOT_TOKEN', '5659616901:AAFGndl7BOLNa1uv1WlELqgGoPt8m7uG')
ADMIN_ID = [int(id) for id in os.getenv('ADMIN_ID', '5938021235').split(',')] #айдишник администратора
ANKET_SEND = [int(id) for id in os.getenv('ANKET_SEND', '5938021235').split(',')] #айдишник, куда будут отсылаться заявки на обмен
SUPPORT_LINK = os.getenv('SUPPORT_LINK', 'https://t.me/multi_coder') #ссылка на саппорта
LINK_SUBSRIBE = os.getenv('LINK_SUBSRIBE', 'https://t.me/multi_coder')
#faq должно быть не больше 4000 символов!
FAQ = F'''
Часто задаваемые вопросы:
Разработчики: https://t.me/weaseldev @weaseldev'''
