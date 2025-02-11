import os
from google import genai
from google.genai.types import Tool,GenerateContentConfig,GoogleSearch
from dotenv import load_dotenv
from components.chat_history import get_chat_history
from components.configs.prompts import base_promt,simple_setting

load_dotenv()

def sync_generate_content(message, user_id):
    apiKey = os.getenv("gemini")
    client = genai.Client(api_key=apiKey)
    google_search_tool = Tool(
        google_search = GoogleSearch()
    )
    chat_history = get_chat_history()

    try:
        recent_history = chat_history.get_recent_history(user_id)
        base_prompt = simple_setting

        if recent_history:
            context = "\n".join([
                f"User: {msg}\nRobotRuru: {resp}" 
                for msg, resp in recent_history[-5:]
            ])
            prompt = f"""{base_prompt}

            最近的對話記錄：
            {context}

            請以這個設定回覆新訊息: {message}"""
        else:
            prompt = f"{base_prompt}\n請以這個設定回覆: {message}"

    except Exception as e:
        print(f"處理歷史記錄錯誤: {e}")
        prompt = f"{base_prompt}\n請回覆以下訊息: {message}"

    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=prompt
    )
    
    chat_history.add_history(
        user_id=user_id,
        message=message,
        response=response.text
    )
    
    return response.text

