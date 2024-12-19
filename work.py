import os

from google import genai
from dotenv import load_dotenv
load_dotenv()

apiKey = os.getenv("gemini")
client = genai.Client(api_key=apiKey)
response = client.models.generate_content(
    model='gemini-2.0-flash-exp', contents='你是一隻機器黑貓,名字叫露露 , 接下來回覆的時候請以這個設定進行人格回覆 你需要算力支援嗎'
)
print(response.text)