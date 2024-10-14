import requests
import random

def get_random_stock():
    # 設定臺灣證券交易所 OpenAPI 的 URL
    api_url = "https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_ALL"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

    high_yield_stocks = [
        stock for stock in data
        if stock['DividendYield'] and float(stock['DividendYield']) > 5 and float(stock['DividendYield']) < 10
    ]
    random_stock = random.choice(high_yield_stocks)
    return random_stock


def get_stock_info(stock_code):
    # 取得股票資訊 日成交資訊
    api_url = f"https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
    response = requests.get(api_url)
    targetData = None
    for data in response.json():
        if data['Code'] == stock_code:
            targetData = data
            break
    return targetData


def getTodayStockDeal():
    api_url = "https://openapi.twse.com.tw/v1/exchangeReport/MI_INDEX20"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        sorted_data = sorted(data, key=lambda x: int(x.get('TradeVolume', '0')), reverse=True)
        max_volume = max(int(item['TradeVolume']) for item in sorted_data)

        result = ["股票交易量排行（單位：萬股）", "=" * 20]

        for item in sorted_data:
            code = item['Code']
            name = item['Name']
            volume = round(int(item['TradeVolume']) / 10000)

            bar_length = int((int(item['TradeVolume']) / max_volume) * 10)
            bar = '\|/' * round(bar_length/3)

            # 使用空格來確保對齊
            formatted_line = f"{code:<6} {name:<10} {volume:>8,} 萬 {bar}"
            result.append(formatted_line)

        result.append("=" * 20)

        return "\n".join(result)

    except requests.RequestException as e:
        return f"請求錯誤: {e}"
    except Exception as e:
        return f"發生未知錯誤: {e}"


def get_random_stock_advise():
    random_stock = get_random_stock()
    stock_name = random_stock['Name']
    stock_code = random_stock['Code']
    stock_dividend_yield = random_stock['DividendYield']
    stock_info = get_stock_info(stock_code)
    stock_today_open = stock_info['OpeningPrice']
    stock_today_high = stock_info['HighestPrice']
    stock_today_low = stock_info['LowestPrice']
    stock_today_close = stock_info['ClosingPrice']
    stock_today_deal = stock_info['Transaction']
    stock_today_change = float(stock_info['Change'])
    warnings = ['韭菜是你','小丑是你','謹慎理財','不要賭博','天臺好冷','我不玩了','把錢還我']

    selected_warnings = random.sample(warnings, 2)

    result = f"{stock_name}\n"
    result += f"{stock_code}\n"
    result += f"殖利率: {stock_dividend_yield}%\n"
    result += f"開盤價: {stock_today_open}\n"
    result += f"收盤價: {stock_today_close}\n"
    result += f"最高價: {stock_today_high}\n"
    result += f"最低價: {stock_today_low}\n"
    result += f"成交量: {stock_today_deal}\n"
    result += f"漲跌: {stock_today_change}\n"
    result += f"{selected_warnings[0]} ,{selected_warnings[1]}\n"
    return result



