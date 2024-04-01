from flask import Flask, request, abort
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from components.tool import *
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

channel_secret = os.getenv("CHANNEL_SECRET")
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座', '魔羯座',
             '水瓶座', '雙魚座']

    if '-w' in text and text.replace('-w','').strip() in astro:
        handle_week_astro(event)
    elif text in astro:
        handle_astro(event)

    elif '--help' in text:
        handle_help(event)

    elif '-抽籤' in text:
        handle_spin(event)

    elif '雷達' == text:
        handle_radar(event)

    elif '抽淺草寺' in text:
        handle_get_ticket(event,'normal')
    elif '抽快樂淺草寺' in text:
        handle_get_ticket(event,'weeeeeee')
    elif text == '盧恩':
        handle_rune(event)
    elif text =='好餓':
        handle_food(event)
    elif '--update' in text :
        handle_updatefood(event)
    elif '--showfoodlist' in text :
        handle_showallfood(event)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
