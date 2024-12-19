from linebot.models import TextSendMessage
from components.ai_Bot import *
from components.chat_history import get_chat_history
from linebot import LineBotApi
from dotenv import load_dotenv
import random
import os
load_dotenv()

channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN")
line_bot_api = LineBotApi(channel_access_token)


def handle_talkState(event):
    text = event.message.text
    user_id = event.source.user_id
    chat_history = get_chat_history()



def handle_ruruTalk(event):
    """對話處理"""
    text = event.message.text
    user_id = event.source.user_id
    chat_history = get_chat_history()

    try:
        # 處理開始對話指令
        if text.strip() == '--talk':
            chat_history.start_chat(user_id)
            response = "喵～露露來陪你聊天啦！想結束對話的話，請說 --talkover 喔！"
            chat_history.add_history(user_id, text, response)
            print(f"開始對話: {user_id}")  # 調試日誌
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response)
            )
            return

        # 處理結束對話指令
        if text.strip() == '--talkover':
            chat_history.end_chat(user_id)
            response = "喵～下次再聊喔！"
            chat_history.add_history(user_id, text, response)
            print(f"結束對話: {user_id}")  # 調試日誌
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response)
            )
            return

        # 更新活動時間
        chat_history.update_activity(user_id)
        
        # 檢查對話狀態
        if not chat_history.is_chatting(user_id):
            print(f"用戶 {user_id} 不在對話模式")  # 調試日誌
            return

        # 生成回應
        response = sync_generate_content(text, user_id)
        
        # 檢查歷史記錄
        print(f"當前對話歷史: {chat_history.get_recent_history(user_id)}")  # 調試日誌
        
        # 發送回應
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

    except Exception as e:
        print(f"Chat Error: {e}")  # 調試日誌
        response = "喵嗚...我好像睡著了"
        chat_history.add_history(user_id, text, response)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )
