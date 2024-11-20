import json
import random
import os

def get_ticket():
    rndNum = random.randint(1,100)
    result = locat_ticket(rndNum)
    return result

def get_good_ticket():
    num = [1, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21, 22, 23, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36,
           37, 38, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 53, 55, 56, 57, 60, 61, 62, 65, 68, 72, 73, 76, 78, 79,
           80, 81, 85, 86, 87, 89, 90, 91, 92, 93, 94, 95, 96, 99]
    rndNum = random.choice(num)
    result = locat_ticket(rndNum)
    return result

def get_fateTicket():
    rndNum = random.randint(1,100)
    message = local_ticket(rndNum)
    imgurl = f'https://storage.googleapis.com/linebot01/gongtiangong/{rndNum}.jpg'
    return message,imgurl
     

def locat_ticket (rndNum):
    def format_result_dict(result_dict):
        formatted_results = []
        for key, value in result_dict.items():
            formatted_results.append(f"{key}：{value}")
        return "\n".join(formatted_results)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'static', 'listenGod.json')
    with open(json_path,'r',encoding='utf-8') as fate :
        content = fate.read()
        fate_data = json.loads(content)
        choose = fate_data[rndNum]
        formatted_num = str(rndNum+1).zfill(3)
        img_url = f'https://storage.googleapis.com/linebot01/img/{formatted_num}.jpg'
        title = f'第{choose['id']}籤'
        type = choose['type']
        poem = choose['poem']
        explain = choose['explain']
        result = format_result_dict(choose['result'])

        returnData = [title,type,poem,explain,result],img_url


    return returnData



def local_ticket(rndNum):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'static', 'fortunes.json')
    imgurl = f'https://www.baishatun.com.tw/31/101/rnd{rndNum}.JPG'
    
    try:
        with open(json_path, 'r', encoding='utf-8') as fate:
            fate_data = json.load(fate)  
            key = str(rndNum)
            fortune = fate_data[key]
           
            
            title = fortune['籤號']
            poems = '\n'.join(fortune['籤詩'])
            explain = fortune['籤意淺釋']
            
   
            divinations = []
            for k, v in fortune['占解'].items():
                if isinstance(v, list):
                    v = '、'.join(v)
                divinations.append(f"{k}：{v}")
            divination_text = '\n'.join(divinations)
            
   
            message = (
                f"【{title}】\n\n"
                f"籤詩：\n{poems}\n\n"
                f"籤意：\n{explain}\n\n"
                f"占解：\n{divination_text}\n\n"
)

            # 如果有字詞說明，加入
            if fortune.get('字詞說明'):
                word_explanations = []
                for k, v in fortune['字詞說明'].items():
                    word_explanations.append(f"{k}：{v}")
                if word_explanations:
                    message += f"字詞說明：\n{''.join(word_explanations)}\n\n"

            # 加入說明部分
            if fortune.get('說明'):
                message += f"說明：\n{fortune['說明']}"
            
            
            return message
            
    except Exception as e:
        print(f"Error: {e}")
        return "抱歉，解籤時出現問題，請重新抽籤。"

