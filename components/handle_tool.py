from linebot.models import TextSendMessage, ImageSendMessage,Sender
from components.astr import *
from components.get_ticket import *
from components.tool_box import *
from components.stock_unit import *
from components.ai_Bot import *
from linebot import LineBotApi
from dotenv import load_dotenv
from plurk_oauth import PlurkAPI
from linebot.models import (
    ButtonComponent,
    MessageAction,
    QuickReply,
    QuickReplyButton,
)
from components.astro_bubble import *
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
             '水瓶座', '雙����座']


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
            # 解析星級和內容
            star_counts = []
            fortune_types = ["整體運勢", "愛情運勢", "事業運勢", "財運運勢"]
            # 處理第一個元素中的所有運勢內容
            content_lines = data[0].split('\n')
            # 取得標題（第二行，因為第一行是空行）
            title = content_lines[1] if len(content_lines) > 1 else f"今日{text}運勢"
            # 處理運勢內容
            for fortune_type in fortune_types:
                found = False
                for line in content_lines:
                    if fortune_type in line:
                        parts = line.split("：", 1)
                        if len(parts) == 2:
                            content = parts[1]
                            star_count = parts[0].count("★")
                            star_counts.append((star_count, content.strip()))
                            found = True
                            break
                if not found:
                    star_counts.append((0, "暫無資料"))

            # 小叮嚀（合併最後一行和第二個元素）
            reminder_parts = []
            if content_lines[-1] and not any(x in content_lines[-1] for x in ["運勢", "解析"]):
                reminder_parts.append(content_lines[-1])
            if len(data) > 1 and data[1].strip():
                reminder_parts.append(data[1])
            reminder = "。".join(part.strip() for part in reminder_parts) if reminder_parts else "今天也要加油喔！"

            # 使用新組件生成 Bubble
            astro_bubble = create_astro_bubble(
                title=title,
                star_counts=star_counts,
                reminder=reminder
            )
            
            flex_message = FlexSendMessage(
                alt_text=f'今日{text}運勢',
                contents=astro_bubble
            )
            
            line_bot_api.reply_message(event.reply_token, flex_message)
            
        except Exception as e:
            print("Error:", e)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="快拿殺蟲劑"))

def handle_week_astro(event):
    text = event.message.text.replace('-w', '').strip()

    if text in astro:
        try:
            data = astr(text)
            # 解析星級和內容
            star_counts = []
            fortune_types = ["整體運勢", "愛情運勢", "事業運勢", "財運運勢"]
            
            # 處理第一個元素中的所有運勢內容
            content_lines = data[0].split('\n')
            
            # 取得標題
            title = f"本週{text}運勢"
            
            # 處理運勢內容
            for fortune_type in fortune_types:
                found = False
                for line in content_lines:
                    if fortune_type in line:
                        parts = line.split("：", 1)
                        if len(parts) == 2:
                            content = parts[1]
                            # 週運沒有星星評分，使用固定值
                            star_count = 3  # 或者可以根據內容關鍵字判斷
                            star_counts.append((star_count, content.strip()))
                            found = True
                            break
                if not found:
                    star_counts.append((0, "暫無資料"))

            reminder_parts = []
            if content_lines[-1] and not any(x in content_lines[-1] for x in ["運勢", "解析"]):
                reminder_parts.append(content_lines[-1])
            if len(data) > 1 and data[1].strip():
                reminder_parts.append(data[1])
            reminder = "。".join(part.strip() for part in reminder_parts) if reminder_parts else "今天也要加油喔！"

            star_parts = []
            for line in content_lines:
                if "速配星座" in line:
                    parts = line.split("：", 1)
                    if len(parts) == 2:
                        star_parts.append(f"本週速配星座：{parts[1].strip()}")
                        break
            
            starreminder = "。".join(part.strip() for part in star_parts) if star_parts else "祝您有個美好的一週！"
            
            # 使用每日運勢的 Bubble 組件
            astro_bubble = create_astro_bubble(
                title=title,
                star_counts=star_counts,
                reminder=reminder,
                starreminder=starreminder
            )
            
            flex_message = FlexSendMessage(
                alt_text=f'本週{text}運勢',
                contents=astro_bubble
            )
            
            line_bot_api.reply_message(event.reply_token, flex_message)
            
        except Exception as e:
            print("Error:", e)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="快拿殺蟲劑"))

def handle_help(event):
    res = (
        "🤖 機器露露使用說明 🤖\n"
        "\n"
        "🔮 星座運勢\n"
        "⭐ 直接輸入星座稱 (例：雙子座)\n"
        "⭐ -w 星座：查看本週運勢\n"
        "⭐ -a 星座：查看完整運勢\n"
        "\n"
        "🎯 抽籤功能\n"
        "⭐ -抽 [問題]\n"
        "⭐ -抽淺草寺 [問題]\n"
        "⭐ -抽快樂淺草寺 [問題]\n"
        "\n"
        "🌤 天氣功能\n"
        "⭐ 輸入「雷達」查看即時天氣\n"
        "\n"
        "🍜 美食推薦\n"
        "⭐ 輸入「好餓」隨機推薦\n"
        "⭐ -隨機 [選項1 選項2 選項3]\n"
        "⭐ --update [Google地圖連結]\n"
        "⭐ --showfoodlist 顯示清單\n"
        "\n"
        "🎲 娛樂功能\n"
        "⭐ --風險骰子\n"
        "\n"
        "���� ��市資訊\n"
        "⭐ --本日韭菜台股前20名\n"
        "⭐ --好想退休：隨機股票建議\n"
        "\n"
        "🔯 紫微斗數\n"
        "⭐ -c 紫微 性別,生日,時辰\n"
        "範例：-c 紫微 1,19931203,12\n"
        "性別：女生0 男生1\n"
        "生日：YYYYMMDD\n"
        "時：24小時制(0-23)\n"
        "\n"
        "💭 想要新功能？\n"
        "歡迎許願！ദി ᷇ᵕ ᷆ )\n"
        "有問題請找開發者～"
    )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=res)
    )


def handle_help_detail(event):
    res = (
        '####以下是機器露露的使用說明####\n\n'
        '【--help】\n'
        '# 說明：\n'
        '毫無反應，就是個說明\n\n'
        '【星座運勢】\n'
        '# 啟動指令：\n'
        '- 輸入星座名稱，例如：雙子座 → 獲得當日運勢\n'
        '- 輸入 -w 星座，例如：-w 雙子座 → 獲得當日&該週運勢\n'
        '- 輸入 -a 星座，例如：-a 雙子座 → 獲得當日&該週運勢\n\n'
        '【國師運勢】\n'
        '# 啟動指令：\n'
        '- 輸入 本週國師 → 獲得國師版該週運勢\n\n'
        '【抽籤功能】\n'
        '# 啟動������：\n'
        '- -抽籤 問題，例如：-抽籤 我可以吃壽司嗎？ → 隨機抽其他籤種\n'
        '- -抽淺草寺 問題，例如：-抽淺草寺 我可以吃烤鴨嗎？ → 回傳籤詩與解籤\n'
        '- -抽快樂淺草寺 問題，例如：-抽快樂淺草寺 我可以吃燒烤嗎？ → 回傳正面籤詩與解籤\n\n'
        '【天氣雷達】\n'
        '# 啟動指令：\n'
        '- 輸入 雷達 → 獲得即時天氣雲圖\n\n'
        '【好餓功能】\n'
        '# 啟動指令：\n'
        '- 輸入 好餓 → 隨機推薦店家（隨機地區）\n'
        '- -隨機 [物件1 物件2 物件3]，例如：-隨機 [壽司 牛排 火鍋] → 隨機挑選一個\n'
        '- --update Google地圖連結，例如：--update 一個吃的Google地圖連結 → 更新至推薦資料庫\n'
        '- --showfoodlist → 列出目前所有食物推薦資料庫\n\n'
        '【風險骰子】\n'
        '# 啟動指令：\n'
        '- 輸入 --風險骰子 → 隨機投擲一個風險骰子\n\n'
        '【本日台股資訊】\n'
        '# 啟動指令：\n'
        '- 輸入 --本日韭菜 → 獲得今日台股交易前20名\n\n'
        '【退休建議】\n'
        '# 啟動指令：\n'
        '- 輸入 --好想退休 → 隨機抓取一個殖利率看起來��行的��的\n'
        '> 謹慎理財，遠離股市，人生自由\n\n'
        '【BETA功能】\n'
        '# 抽白沙屯：\n'
        '- 輸入 抽白沙屯 → 獲得白沙屯媽祖籤詩\n\n'
        '【紫微解盤】\n'
        '# 啟動指令：\n'
        '- -c 紫微 性別,出生年月日,時辰\n\n'
        '性別：女生0；男生1\n'
        '出生年月日：yyyymmdd\n'
        '時辰：24小時制（0~24）\n'
        '範例：\n'
        '- 男1993年12月3號，中午十二點生\n'
        '-c 紫微 1,19931203,12\n'
        '- 女1999年2月15號，晚上九點生\n'
        '-c 紫微 0,19990215,21\n\n'
        '############\n'
        '有什麼想要的功能可以許願，但不一定能實現 ദി ᷇ᵕ ᷆ )\n'
        '如果遭遇任何問題請聯繫開發者，我相信可以找到的吧?\n'
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
        error = TextSendMessage(text='���過段時間後再次嘗試')
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

    line_bot_api.reply_message(event.reply_token, image_message)

def handle_ziwei(event):
    text = event.message.text.replace('-c 紫微', '').strip()
    processdata = text.split(',')
    res = process_ziwei(processdata)
    text_message = TextSendMessage(text=res)
    line_bot_api.reply_message(event.reply_token, text_message)


def handle_new_help(event):
    is_group = hasattr(event.source, 'group_id')
    
    help_bubble = BubbleContainer(
        size='mega',
        styles={
            "header": {"backgroundColor": "#27ACB2"},
            "body": {"backgroundColor": "#ffffff"},
            "footer": {"backgroundColor": "#f5f5f5"}
        },
        header=BoxComponent(
            layout='vertical',
            paddingAll='md',
            backgroundColor='#27ACB2',
            contents=[
                TextComponent(
                    text="🤖 機器露露功能表",
                    weight='bold',
                    size='md',
                    align='center',
                    color='#ffffff'
                )
            ]
        ),
        body=BoxComponent(
            layout='vertical',
            paddingAll='md',
            paddingTop='xs',
            spacing='xs',
            contents=[
                # 常用功能區
                BoxComponent(
                    layout='horizontal',
                    margin='xs',
                    contents=[
                        ButtonComponent(
                            style='primary',
                            color='#27ACB2',
                            action=MessageAction(
                                label="天��",
                                text="雷達"
                            ),
                            flex=1,
                            margin='sm'
                        ),
                        ButtonComponent(
                            style='primary',
                            color='#27ACB2',
                            action=MessageAction(
                                label="抽籤",
                                text="抽淺草寺"
                            ),
                            flex=1,
                            margin='sm'
                        ),
                        ButtonComponent(
                            style='primary',
                            color='#27ACB2',
                            action=MessageAction(
                                label="看股市",
                                text="--本日韭菜"
                            ),
                            flex=1,
                            margin='sm'
                        )

                    ]
                ),
                # 分隔線
                BoxComponent(
                    layout='vertical',
                    margin='xs',
                    contents=[
                        TextComponent(text='-'*40, color='#E0E0E0', size='xs', align='center')
                    ]
                ),
                # 星座功能
                BoxComponent(
                    layout='baseline',
                    spacing='sm',
                    contents=[
                        TextComponent(text="🧙", size='md', flex=1),
                        TextComponent(text="各種抽籤", weight='bold', size='sm', color='#27ACB2', flex=3),
                        TextComponent(text="直接輸入抽什麼籤跟問題\n-抽淺草寺 [問題]\n-抽白沙屯 [問題]\n-抽籤 問題",
                                      size='sm', wrap=True, flex=6)
                    ]
                ),
                BoxComponent(
                    layout='baseline',
                    spacing='sm',
                    contents=[
                        TextComponent(text="🔮", size='md', flex=1),
                        TextComponent(text="星座運勢", weight='bold', size='sm', color='#27ACB2', flex=3),
                        TextComponent(text="直接輸入星座名稱\n-w [星座] 週運\n-a [星座] 整運勢\n本週國師",
                                    size='sm', wrap=True, flex=6)
                    ]
                ),
                BoxComponent(
                    layout='baseline',
                    spacing='sm',
                    contents=[
                        TextComponent(text="🔭", size='md', flex=1),
                        TextComponent(text="紫微解盤", weight='bold', size='sm', color='#27ACB2', flex=3),
                        TextComponent(text="輸入-c 紫微 \n,性別,yyyymmdd,時辰\n日期：yyyymmdd\n性別：男:1;女:0\n時辰：0~23",
                                      size='sm', wrap=True, flex=6)
                    ]
                ),
                BoxComponent(
                    layout='vertical',
                    margin='md',
                    backgroundColor='#F8F9FA',
                    paddingAll='md',
                    cornerRadius='md',
                    contents=[
                        TextComponent(
                            text="📝 常用指令範例",
                            weight='bold',
                            size='sm',
                            color='#27ACB2'
                        ),
                        TextComponent(
                            text="雙子座\n-w 天蠍座\n-抽淺草寺 明天會下雨嗎\n-隨機 麵 滷肉飯 義大利麵",
                            size='xs',
                            margin='md',
                            wrap=True
                        )
                    ]
                ),

            ]
        ),
        footer=BoxComponent(
            layout='vertical',
            spacing='sm',
            contents=[
                ButtonComponent(
                    style='secondary',
                    action=MessageAction(
                        label="🎲 風險骰子",
                        text="--風險骰子"
                    )
                ),
                ButtonComponent(
                    style='secondary',
                    action=MessageAction(
                        label="🔮 抽淺草寺",
                        text="-抽淺草寺 運勢"
                    )
                ),
                ButtonComponent(
                    style='secondary',
                    action=MessageAction(
                        label="👀 詳細說明",
                        text="-d-i help"
                    )
                ),

                TextComponent(
                    text="💭 想要新功能？歡迎許願！",
                    size='sm',
                    align='center',
                    color='#888888',
                    margin='md'
                )
            ]
        )
    )

    # 只在私聊時加入快速回覆
    if not is_group:
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="天氣", text="雷達")),
                QuickReplyButton(action=MessageAction(label="美食", text="好餓")),
                QuickReplyButton(action=MessageAction(label="股市", text="--本日韭菜")),
                QuickReplyButton(action=MessageAction(label="紫微", text="-c 紫微 1,19931203,12"))
            ]
        )
        flex_message = FlexSendMessage(
            alt_text='機器露露使用說明',
            contents=help_bubble,
            quick_reply=quick_reply
        )
    else:
        flex_message = FlexSendMessage(
            alt_text='機器露露使用說明',
            contents=help_bubble
        )

    line_bot_api.reply_message(event.reply_token, flex_message)

