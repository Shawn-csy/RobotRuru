
from linebot.models import TextSendMessage, ImageSendMessage,Sender
from components.astr import *
from components.get_ticket import *
from components.tool_box import *
from components.stock_unit import *
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
astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座', '魔羯座',
             '水瓶座', '雙魚座']


def handle_all_astro(event):
    text = event.message.text.replace('-a','').strip()

    if text in astro:
        try:
            dayData = astr_today(text)
            dayData.insert(0, '')
            Dayresponse = ''.join(dayData)
            weekdata = astr(text)
            weekres = ''.join(weekdata)
            res = Dayresponse + "\n" + weekres
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=res))


        except Exception as e :
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="快拿殺蟲劑"))





def handle_astro(event):

    text = event.message.text
    if text in astro:
        try:
            data = astr_today(text)

            data.insert(0,'')
            response = ''.join(data)
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage
                                       (text=response,
                                        # sender=sendertool[0]
                                        ))
        except Exception as e:
            print("Error:", e)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="快拿殺蟲劑"))


def handle_week_astro(event):

    text = event.message.text.replace('-w', '').strip()

    if text in astro:
        try:
            data = astr(text)
            response = data
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response[0]))
        except Exception as e:
            print("Error:", e)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="快拿殺蟲劑"))


def handle_help(event):
    res = (
        '####以下是機器露露的使用說明####\n\n'
        '## --help\n'
        '毫無反應,就是個說明\n\n'
        '## 輸入星座\n'
        '(像是 雙子座 )\n'
        '獲得該天運勢\n\n'
        '## 輸入-w 星座\n'
        '(像是-w 雙子座)\n'
        '## 輸入-a 星座\n'
        '(像是-a 雙子座)\n'
        '獲得當天&該週運勢\n\n'
        '## 輸入 本週國師\n'
        '獲得國師版該週運勢\n\n'
        '## -抽籤\n'
        '(像是-抽籤 我可以吃壽司嗎？)\n'
        '抽不是淺草籤的其他籤種\n\n'
        '## 抽淺草寺\n'
        '(像是-抽淺草寺 我可以吃烤鴨嗎？)\n'
        '回傳籤詩跟解籤\n\n'
        '## 抽快樂淺草寺\n'
        '(像是-抽快樂淺草寺 我可以吃燒烤嗎？)\n'
        '只會回傳正面的籤詩跟解籤\n\n'
        '#################\n\n'
        '## 雷達\n'
        '獲得即時天氣雲圖\n\n'
        '## 好餓\n'
        '獲得隨機推薦店家(隨機地區,對)\n\n'
        '## - 輸入`-隨機 [ 物件 物件 物件 ]` \n'
        '從物件中隨機挑選一個輸出, 可使用空格或,分隔\n\n'
        '## --update googlemap連結\n'
        '(像是--update 一個吃的google連結)\n'
        '更新進推薦資料庫\n\n'
        '## --showfoodlist\n'
        '羅列目前所有的食物推薦資料庫\n\n'
         '## --風險骰子\n'
        '隨機投擲一個風險骰子\n\n'
         '## --本日韭菜\n'
        '輸入“--本日韭菜” 獲得今日台股交易前20名\n\n'
        '## --好想退休\n'
        '輸入“--好想退休” 隨機抓取一個殖利率看起來還行的東西\n\n'
        '謹慎理財 不要賭博 遠離股市 人生自由\n\n'
        '#######BETA功能#####\n'
        '## 抽白沙屯\n'
        '輸入“抽白沙屯” 獲得白沙屯媽祖籤詩\n\n'
        '# 使用紫微解盤\n'
        '# 使用紫微解盤時需特別注意如何使用\n'
        '## -c 紫微 性別,出生年月日,時辰\n'
        '性別：女為0,男為1\n'
        '出生年月日：西元四碼+兩碼月+兩碼日\n'
        '時辰：使用一天24小時制\n'
        '使用範例：\n'
        '男1993年12月3號,中午十二點生：-c 紫微 1,19931203,12\n'
        '女1999年2月15號,晚上九點生：-c 紫微 0,19990215,21\n\n'
        '############\n'
        '有什麼想要的功能可以許願但不一定能實現ദി  ᷇ᵕ  ᷆  )\n'
        '如果遭遇任何問題請聯繫開發者,我相信可以找到的吧?\n'

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

def handle_fate_ticket(event):
    data = get_fateTicket()
    message,img_url = data
    
    text_message = TextSendMessage(text=message)
    image_message = ImageSendMessage(
        original_content_url=img_url,
        preview_image_url=img_url
    )

    line_bot_api.reply_message(event.reply_token, [image_message, text_message])


def handle_get_ticket(event, type):
    if type == 'normal':
        data = get_ticket()
    else:
        data = get_good_ticket()

    ticket_info, img_url = data
    title, ticket_type, poem, explain, result = ticket_info
    content = f"{title}\n" \
              f"***{ticket_type}***\n\n" \
              f"籤詩：\n{poem}\n\n" \
              f"解籤：\n{explain}\n\n" \
              f"結果：\n{result}"

    text_message = TextSendMessage(text=content)
    image_message = ImageSendMessage(
        original_content_url=img_url,
        preview_image_url=img_url
    )

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

def handle_rich_dice(event):
    data = rich_dice(event)
    image_message = ImageSendMessage(original_content_url=data, preview_image_url=data)
    line_bot_api.reply_message(event.reply_token, image_message)


def handle_stock_data(event):
    data = getTodayStockDeal()
    text_message = TextSendMessage(text=data)
    line_bot_api.reply_message(event.reply_token,text_message)

def handle_stock_advise(event):
    data = get_random_stock_advise()
    text_message = TextSendMessage(text=data)
    line_bot_api.reply_message(event.reply_token,text_message)


def handle_qrcode (event):
    text = event.message.text.replace('-qrcode', '').strip()
    qr_url = f"https://ruru-api-558195193094.asia-east1.run.app/ctqrcode?qrcode_data={text}.png"

    image_message = ImageSendMessage(original_content_url=qr_url, preview_image_url=qr_url)
    replyText = f"以下是qrCode包含的資訊:{text}"
    text_message = TextSendMessage(text=replyText)
    # line_bot_api.reply_message(event.reply_token, text_message)
    print(qr_url)
    line_bot_api.reply_message(event.reply_token, image_message)

def handle_ziwei(event):
    text = event.message.text.replace('-c 紫微', '').strip()
    processdata = text.split(',')
    res = process_ziwei(processdata)
    text_message = TextSendMessage(text=res)
    line_bot_api.reply_message(event.reply_token, text_message)


# def handle_stock_opt(event):
#     inputdata = event.message.text
#     par = inputdata.split(" ")
#     random_par = par(1)
#     text_message = TextSendMessage(text=data)
#     line_bot_api.reply_message(event.reply_token, text_message)