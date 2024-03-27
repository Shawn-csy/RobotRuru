from flask import Flask, request, abort
from components.astr import astr,randomspin
from components.plurk import plurktest
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("CHANNEL_SECRET")
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# Webhook route configuration
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Handle text messages
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座', '魔羯座',
             '水瓶座', '雙魚座']
    text = event.message.text
    if text in astro:
        data = astr(text)
        print(data)
        response = '\n'.join(data)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )
    if '-抽籤' in text :
        data = randomspin()
        response = '\n'.join(data)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )
    if text == 'tttest':
        data = plurktest()
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url=data,
                             preview_image_url=data)
        )






# Handle image messages
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # Get the ID of the image message
    message_id = event.message.id
    try:
        # Get image content using LineBotApi
        message_content = line_bot_api.get_message_content(message_id)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url="https://images.plurk.com/5ONykMAH1UKK3TUWl8zUY7.png", preview_image_url="https://images.plurk.com/5ONykMAH1UKK3TUWl8zUY7.png")
        )
    except LineBotApiError as e:
        print("LineBotApiError:", e)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3030)
