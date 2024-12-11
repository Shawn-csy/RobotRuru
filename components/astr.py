import random

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def astr(i):
    today = datetime.today().strftime('%Y-%m-%d')
    astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座', '魔羯座',
             '水瓶座', '雙魚座', ]
    index = astro.index(i)
    url = f'https://astro.click108.com.tw/weekly_1.php?iAcDay={today}&iType=1&iAstro={index}'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    today_word_elements = soup.find_all('div', class_='TODAY_WORD', )
    todayFeature = soup.find_all('div', class_='TODAY_CONTENT')
    data = []
    for i in todayFeature:
        data.append(i.text)
    for i in today_word_elements:
        p_tags = i.find_all('p')
        for j in p_tags:
            data.append(j.text)

    return data

def astr_today(i):
    today = datetime.today().strftime('%Y-%m-%d')
    astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座', '魔羯座',
             '水瓶座', '雙魚座', ]
    index = astro.index(i)
    url = f'https://astro.click108.com.tw/daily_0.php?iAstro={index}&iAcDay={today}'

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    today_word_elements = soup.find_all('div', class_='TODAY_WORD', )
    todayFeature = soup.find_all('div', class_='TODAY_CONTENT')
    data = []
    for i in todayFeature:
        data.append(i.text)
    for i in today_word_elements:
        p_tags = i.find_all('p')
        for j in p_tags:
            data.append(j.text)

    return data


def weeklyfate():
    url = "https://podcasts.apple.com/tw/podcast/%E5%94%90%E9%99%BD%E9%9B%9E%E9%85%92%E5%B1%8B/id1536374746"
    res = requests.get(url)


    if res.status_code != 200:
        return None

    def timedefine(podcasttime):
        try:

            date_time1 = datetime.today()
            date_time2 = datetime.strptime(podcasttime, "%Y-%m-%d")
            difference = date_time1 - date_time2
            return difference.days
        except ValueError as ve:
            return None

    html_content = res.content.decode()
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find("script", {"id": "schema:show"})


    if not script_tag:
        return None

    try:
        json_data = script_tag.string
        podcast_info = json.loads(json_data)
        workdata = podcast_info['workExample']
        for item in workdata:
            if "【本週提醒】" in item["name"]:
                days_diff = timedefine(item["datePublished"])
                if days_diff is not None and days_diff < 8:
                    return item['description']
        return "本週還沒有提醒～"
    except json.JSONDecodeError as je:
        return None
    except KeyError as ke:
        return None



def get_ziwei_fate(sex, year, month, day, hour, calendar_type=1, leap_month=''):
    form_data = {
        'Nickname': random.randint(0,9987),
        'iSex': str(sex),  
        'iCalendar': str(calendar_type),
        'iYear': str(year),
        'iMonth': str(month),
        'iDay': str(day),
        'iHour': str(hour),
        'LeapMonth': leap_month
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.click108.com.tw/unit001/free-ziwei/index.php'
    }
    
    try:
        response = requests.post(
            'https://www.click108.com.tw/unit001/free-ziwei/result.php',
            data=form_data,
            headers=headers
        )
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        content_paragraphs = soup.find_all('p', class_='pq_TXT3')
        
        if content_paragraphs:
            parsed_data = {
                "命盤基礎": {
                    "命宮": {
                        "主星": None,
                        "類型": None,
                        "特質": [],
                        "優點": [],
                        "缺點": [],
                        "建議": None,
                        "完整描述": None
                    },
                    "夫妻宮": {
                        "主星": None,
                        "類型": None,
                        "特質": [],
                        "感情態度": [],
                        "擇偶傾向": [],
                        "婚姻特點": [],
                        "完整描述": None
                    },
                    "事業宮": {
                        "主星": None,
                        "類型": None,
                        "特質": [],
                        "學習特點": [],
                        "工作態度": [],
                        "事業發展": [],
                        "完整描述": None
                    },
                    "財帛宮": {
                        "主星": None,
                        "類型": None,
                        "特質": [],
                        "理財方式": [],
                        "投資特點": [],
                        "財運分析": [],
                        "完整描述": None
                    },
                    "子女宮": {
                        "主星": None,
                        "類型": None,
                        "特質": [],
                        "教育方式": [],
                        "親子關係": [],
                        "完整描述": None
                    }
                },
                "運勢分析": {
                    "大運": {
                        "當前階段": None,
                        "年齡區間": None,
                        "宮位": None,
                        "特徵": [],
                        "機會": [],
                        "挑戰": [],
                        "完整描述": None
                    },
                    "流年": {
                        "年份": None,
                        "宮位": None,
                        "重點提醒": [],
                        "完整描述": None
                    },
                    "小限": {
                        "當前年齡": None,
                        "主星": None,
                        "能量轉變": [],
                        "特徵": [],
                        "完整描述": None
                    }
                }
            }

            # 解析文本
            for p in content_paragraphs:
                text = p.get_text(strip=True)

                # 命宮解析
                if "你的命宮主星是" in text:
                    parts = text.split("，屬於")
                    parsed_data["命盤基礎"]["命宮"]["主星"] = parts[0].replace("你的命宮主星是", "").strip()
                    parsed_data["命盤基礎"]["命宮"]["類型"] = parts[1].split("，")[0].strip()

                    # 提取特質
                    traits = text.split("，")[2:]
                    for trait in traits:
                        if "你是" in trait:
                            parsed_data["命盤基礎"]["命宮"]["特質"].append(trait.replace("你是", "").strip())
                        elif "不過" in trait:
                            parsed_data["命盤基礎"]["命宮"]["缺點"].append(trait.replace("不過", "").strip())
                        elif "如果" in trait:
                            parsed_data["命盤基礎"]["命宮"]["建議"] = trait.strip()

                    parsed_data["命盤基礎"]["命宮"]["完整描述"] = text

                # 夫妻宮解析
                elif "你的夫妻宮主星是" in text:
                    parts = text.split("，屬於")
                    parsed_data["命盤基礎"]["夫妻宮"]["主星"] = parts[0].replace("你的夫妻宮主星是", "").strip()
                    parsed_data["命盤基礎"]["夫妻宮"]["類型"] = parts[1].split("，")[0].strip()

                    # 提取感情特質
                    traits = text.split("；")
                    for trait in traits:
                        if "異性緣" in trait:
                            parsed_data["命盤基礎"]["夫妻宮"]["感情態度"].append(trait.strip())
                        elif "欣賞" in trait:
                            parsed_data["命盤基礎"]["夫妻宮"]["擇偶傾向"].append(trait.strip())

                    parsed_data["命盤基礎"]["夫妻宮"]["完整描述"] = text

                # 事業宮解析
                elif "你的事業宮主星是" in text:
                    parts = text.split("，屬於")
                    parsed_data["命盤基礎"]["事業宮"]["主星"] = parts[0].replace("你的事業宮主星是", "").strip()
                    parsed_data["命盤基礎"]["事業宮"]["類型"] = parts[1].split("，")[0].strip()

                    # 提取學習特點
                    traits = text.split("，")[2:]
                    for trait in traits:
                        if "你學習" in trait:
                            parsed_data["命盤基礎"]["事業宮"]["學習特點"].append(trait.replace("你學習", "").strip())
                        elif "你工作" in trait:
                            parsed_data["命盤基礎"]["事業宮"]["工作態度"].append(trait.replace("你工作", "").strip())

                    parsed_data["命盤基礎"]["事業宮"]["完整描述"] = text

                # 財帛宮解析
                elif "你的財帛宮主星是" in text:
                    parts = text.split("，屬於")
                    parsed_data["命盤基礎"]["財帛宮"]["主星"] = parts[0].replace("你的財帛宮主星是", "").strip()
                    parsed_data["命盤基礎"]["財帛宮"]["類型"] = parts[1].split("，")[0].strip()

                    # 提取理財方式
                    traits = text.split("，")[2:]
                    for trait in traits:
                        if "你理財" in trait:
                            parsed_data["命盤基礎"]["財帛宮"]["理財方式"].append(trait.replace("你理財", "").strip())
                        elif "你投資" in trait:
                            parsed_data["命盤基礎"]["財帛宮"]["投資特點"].append(trait.replace("你投資", "").strip())

                    parsed_data["命盤基礎"]["財帛宮"]["完整描述"] = text

                # 子女宮解析
                elif "你的子女宮主星是" in text:
                    parts = text.split("，屬於")
                    parsed_data["命盤基礎"]["子女宮"]["主星"] = parts[0].replace("你的子女宮主星是", "").strip()
                    parsed_data["命盤基礎"]["子女宮"]["類型"] = parts[1].split("，")[0].strip()

                    # 提取教育方式
                    traits = text.split("，")[2:]
                    for trait in traits:
                        if "你教育" in trait:
                            parsed_data["命盤基礎"]["子女宮"]["教育方式"].append(trait.replace("你教育", "").strip())
                        elif "你親子" in trait:
                            parsed_data["命盤基礎"]["子女宮"]["親子關係"].append(trait.replace("你親子", "").strip())

                    parsed_data["命盤基礎"]["子女宮"]["完整描述"] = text

                # 大運解析
                elif "目前你正走在人生的" in text:
                    parsed_data["運勢分析"]["大運"]["當前階段"] = text.split("，")[0].replace("目前你正走在人生的", "").strip()
                    if "(23-32歲)" in text:
                        parsed_data["運勢分析"]["大運"]["年齡區間"] = "23-32歲"
                    if "走到" in text:
                        parsed_data["運勢分析"]["大運"]["宮位"] = text.split("走到")[1].split("，")[0].strip()
                    parsed_data["運勢分析"]["大運"]["完整描述"] = text

                # 流年解析
                elif "年即將到來" in text:
                    parsed_data["運勢分析"]["流年"]["年份"] = "2025年"
                    if "走到" in text:
                        parsed_data["運勢分析"]["流年"]["宮位"] = text.split("走到")[1].split("，")[0].strip()
                    parsed_data["運勢分析"]["流年"]["完整描述"] = text

                # 小限解析
                elif "你目前" in text and "歲所行小限" in text:
                    age_part = text.split("歲所行小限")[0]
                    parsed_data["運勢分析"]["小限"]["當前年齡"] = age_part.replace("你目前", "").strip()
                    if "主星是" in text:
                        parsed_data["運勢分析"]["小限"]["主星"] = text.split("主星是")[1].split("，")[0].strip()
                    parsed_data["運勢分析"]["小限"]["完整描述"] = text

            return {
                'parsed': parsed_data,
                'paragraphs': [p.get_text(strip=True) for p in content_paragraphs],
                'full_text': '\n'.join([p.get_text(strip=True) for p in content_paragraphs]),
                'raw_html': [str(p) for p in content_paragraphs]
            }
            
    except Exception as e:
        return {'error': f'格式錯誤: 請依照 性別(0or1),西元年月日(八碼),24小時制'}


def process_ziwei(processdata):
    try:
        # 檢查參數數量
        if len(processdata) != 3:
            return "格式錯誤\n正確格式為: -c 紫微 性別,出生年月日,時辰\n例: -c 紫微 1,19931203,12"
        # 驗證性別
        sex = processdata[0]
        if sex not in ['0', '1']:
            return "性別格式錯誤\n女性請輸入0\n男性請輸入1"

        # 驗證日期格式
        try:
            birth_date = processdata[1]
            if len(birth_date) != 8:
                raise ValueError("出生日期格式錯誤")

            year = birth_date[0:4]
            month = birth_date[4:6]
            day = birth_date[6:8]

            # 轉換為整數進行驗證
            year_int = int(year)
            month_int = int(month)
            day_int = int(day)
            if year_int < 1900 or year_int > int(datetime.today().year):
                return "年份需介於1900~今年"

            if month_int < 1 or month_int > 12:
                return "月份必須在1-12之間"


            if day_int < 1 or day_int > 31:
                return "日期必須在1-31之間"

            # 驗證時辰
            hour = int(processdata[2])
            if hour < 0 or hour > 23:
                return "時辰必須在0-23之間"


        except ValueError:
            return "日期格式錯誤\n請使用8位數字，例如:19931203"


        # 通過驗證後的處理邏輯
        data = {"sex": sex, "year": year, "month": month, "day": day, "hour": processdata[2]}
        fate_data = get_ziwei_fate(data['sex'], data["year"], data["month"], data["day"], data["hour"])['parsed']
        free_fate = fate_data['命盤基礎']
        future_fate = fate_data["運勢分析"]
        res = (
            "=== 紫微命盤解析 ===\n\n"
            f"★ 命宮解析\n{free_fate['命宮']['完整描述']}\n\n"
            f"★ 夫妻宮解析\n{free_fate['夫妻宮']['完整描述']}\n\n"
            f"★ 事業宮解析\n{free_fate['事業宮']['完整描述']}\n\n"
            f"★ 財帛宮解析\n{free_fate['財帛宮']['完整描述']}\n\n"
            f"★ 子女宮解析\n{free_fate['子女宮']['完整描述']}\n\n"
            "=== 運勢分析 ===\n\n"
            f"★ 大運\n{future_fate['大運']['完整描述']}\n\n"
            f"★ 流年\n{future_fate['流年']['完整描述']}\n\n"
            f"★ 小限\n{future_fate['小限']['完整描述']}\n\n"
            "==================\n"
            "（解析來自科技紫微網）\n"
            "（還想怎樣）\n"
        )
        parse_res = res.replace('...', "「免費仔知道這些就夠了」")
        return  parse_res

    except ValueError:
        return "日期格式錯誤\n請使用8位數字，例如:19931203"
