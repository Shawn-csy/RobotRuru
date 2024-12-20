from flask import Flask, request, abort
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from components.handle_tool import *
from components.handle_ai import *
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
    user_id = event.source.user_id
    chat_history = get_chat_history()
    
    # 檢查是否在聊天模式
    if chat_history.is_chatting(user_id) or text.strip() in ['!請神符', '!送神符'] or text.startswith('!請神符'):
        # 檢查是否為特殊指令並執行
        command_executed = handle_special_commands(event)
        
        # 如果沒有執行特殊指令，才使用 AI 回應
        if not command_executed:
            handle_ruruTalk(event)
        return

    # 一般指令處理
    command_executed = handle_special_commands(event)
    if not command_executed:
        handle_ruruTalk(event)

def handle_special_commands(event):
    """處理所有特殊指令，返回是否已處理"""
    text = event.message.text
    
    # 指令映射表
    command_handlers = {
        '--help': handle_help,
        '--newhelp': handle_new_help,
        '-d-i help': handle_help_detail,
        '-抽籤': handle_spin,
        '雷達': handle_radar,
        '本週國師': handle_weekfate,
        '好餓': handle_food,
        '--update': handle_updatefood,
        '--showfoodlist': handle_showallfood,
        '-隨機': handle_random_box,
        '風險骰子': handle_rich_dice,
        '--本日韭菜': handle_stock_data,
        '--好想退休': handle_stock_advise,
        '-qrcode': handle_qrcode
    }

    # 檢查一般指令
    if text in command_handlers:
        command_handlers[text](event)
        return True

    # 星座相關指令處理
    astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', 
             '天秤座', '天蠍座', '射手座', '魔羯座', '水瓶座', '雙魚座']
    
    if text in astro:
        handle_astro(event)
        return True
    
    if '-w' in text and text.replace('-w','').strip() in astro:
        handle_week_astro(event)
        return True
        
    if '-a' in text and text.replace('-a','').strip() in astro:
        handle_all_astro(event)
        return True

    # 抽籤相關指令處理
    if '抽淺草寺' in text:
        handle_get_ticket(event, 'normal' if '快樂' not in text else 'weeeeeee')
        return True
        
    if '抽白沙屯' in text:
        handle_fate_ticket(event)
        return True

    # 紫微斗數處理
    if '-c 紫微' in text:
        handle_ziwei(event)
        return True

    return False


if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=8080)
