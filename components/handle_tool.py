
from linebot.models import TextSendMessage, ImageSendMessage
from components.astr import *
from components.get_ticket import *
from components.tool_box import *
from linebot import LineBotApi
from dotenv import load_dotenv
from plurk_oauth import PlurkAPI
import random
import os
load_dotenv()
#Line Part
channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("CHANNEL_SECRET")

#Plurk Part
CONSUMER_KEY = os.getenv('plurk_App_key')
CONSUMER_SECRET = os.getenv('plurk_App_secret')
ACCESS_TOKEN = os.getenv('plurk_token')
ACCESS_TOKEN_SECRET = os.getenv('plurk_secret')

line_bot_api = LineBotApi(channel_access_token)
plurk = PlurkAPI(CONSUMER_KEY, CONSUMER_SECRET)
plurk.authorize(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def handle_astro(event):
    astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座', '魔羯座',
             '水瓶座', '雙魚座']
    text = event.message.text
    if text in astro:
        try:
            data = astr_today(text)
            data.insert(0,'\n')
            response = '\n'.join(data)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        except Exception as e:
            print("Error:", e)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\BUG/,請聯繫開發者"))


def handle_week_astro(event):
    astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座', '魔羯座',
             '水瓶座', '雙魚座']
    text = event.message.text.replace('-w', '').strip()

    if text in astro:
        try:
            data = astr(text)
            response = '\n'.join(data)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        except Exception as e:
            print("Error:", e)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\BUG/,請聯繫開發者"))


def handle_help(event):
    res = (
        '## --help\n'
        '毫無反應,就是個說明\n\n'
        '## 輸入星座\n'
        '獲得該天運勢\n\n'
        '## 輸入-w 星座\n'
        '獲得該週運勢\n\n'
        '## 輸入 本週國師\n'
        '獲得國師版該週運勢\n\n'
        '## -抽籤\n'
        '抽非淺草簽\n\n'
        '## 抽淺草寺\n'
        '回傳籤詩跟解籤\n\n'
        '## 抽快樂淺草寺\n'
        '回傳籤詩跟解籤\n\n'
        '#################\n'
        '## 雷達\n'
        '獲得即時天氣雲圖\n\n'
        '## 好餓\n'
        '獲得隨機推薦店家\n\n'
        '## - 輸入`-隨機 [ 物件 物件 物件 ]` \n'
        '從物件中隨機挑選一個輸出, 可使用空格或,分隔\n\n'
        '## --update googlemap連結\n'
        '更新進推薦資料庫\n'
        '## --showfoodlist\n'
        '羅列目前所有的食物推薦資料庫'
    )
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=res)
    )

def handle_spin(event):
    data = randomspin()
    data.append('\nRef: https://iwnet.civil.taipei/SignedPoetry')
    response = '\n'.join(data)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

def handle_radar(event):
    data = radar()
    image_message = ImageSendMessage(original_content_url=data[0], preview_image_url=data[0])
    line_bot_api.reply_message(event.reply_token, image_message)

def handle_get_ticket(event,type):
    if type =='normal':
        data = get_ticket()
    else:
        data = get_good_ticket()

    content = '\n'.join(data[0])
    img = data[1]
    text_message = TextSendMessage(text=content)
    image_message = ImageSendMessage(original_content_url=img, preview_image_url=img)
    line_bot_api.reply_message(event.reply_token, [image_message, text_message])

def handle_rune(event):
    data = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Runic_letter_laukaz.svg/24px-Runic_letter_laukaz.svg.png'
    image_message = ImageSendMessage(original_content_url=data, preview_image_url=data)
    line_bot_api.reply_message(event.reply_token, image_message)

def handle_food(event):
    try:
        data = plurk.callAPI('/APP/Responses/get', {"plurk_id": "348756189077988"})
        food_list = data['responses']
        rnd_food = random.randint(1, len(food_list)) - 1
        choose = data['responses'][rnd_food]
        url = TextSendMessage(text=choose['content_raw'])
        title = TextSendMessage(text=BeautifulSoup(choose['content'], 'html.parser').a.text)
        line_bot_api.reply_message(event.reply_token, [title, url])
    except:
        error = TextSendMessage(text='請過段時間後再次嘗試')
        line_bot_api.reply_message(event.reply_token, error)

def handle_updatefood(event):
    updateData = event.message.text.replace('##update','').strip()
    plurk.callAPI('/APP/Responses/responseAdd',
                        {"plurk_id": "348756189077988", "content": f"{updateData}", 'qualifier': '1'})
    text_message = TextSendMessage(text=updateData+'已經加入食物串啦～')
    line_bot_api.reply_message(event.reply_token, text_message)

def handle_showallfood(event):
    data = plurk.callAPI('/APP/Responses/get', {"plurk_id": "348756189077988"})
    res = ""
    food_list = data['responses']
    for index, food in enumerate(food_list):
        url = food['content_raw']
        title = BeautifulSoup(food['content'], 'html.parser').a.text
        res += f"{index + 1}：\n{title}\n{url}\n\n"

    text_message = TextSendMessage(text=res)
    line_bot_api.reply_message(event.reply_token, text_message)

def handle_weekfate(event):
    data = weeklyfate()
    text_message = TextSendMessage(text=data)
    line_bot_api.reply_message(event.reply_token, text_message)


def handle_random_box(event):
    data = random_box(event)
    text_message = TextSendMessage(text=data)
    line_bot_api.reply_message(event.reply_token, text_message)


