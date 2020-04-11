import telegram
import os


class Sender():
    def __init__(self):
        self.bot = telegram.Bot(token=os.environ['TELEGRAM_SEC'])
        self.chat_id = int(os.environ['CHATID'])

    def send_telegram_msg(self, ):
        self.bot.sendMessage(chat_id=self.chat_id, text='구매성공')
