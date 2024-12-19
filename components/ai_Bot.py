import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from components.chat_history import get_chat_history

load_dotenv()

def sync_generate_content(message, user_id):
    apiKey = os.getenv("gemini")
    client = genai.Client(api_key=apiKey)
    chat_history = get_chat_history()

    try:
        recent_history = chat_history.get_recent_history(user_id)
        # 基礎設定和完整功能說明
        base_prompt = """你是一隻機器黑貓,名字叫露露。
        請用貓咪AI的語氣回應。
        """

        if recent_history:
            context = "\n".join([
                f"User: {msg}\nLulu: {resp}" 
                for msg, resp in recent_history
            ])
            prompt = f"""{base_prompt}

            以下是之前的對話：
            {context}

            請以這個設定回覆新訊息: {message}"""
        else:
            prompt = f"{base_prompt}\n請以這個設定回覆: {message}"

    except Exception as e:
        
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

