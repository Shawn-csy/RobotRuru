import requests
from bs4 import BeautifulSoup
import json

def get_fortune(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 提取籤號
        title = soup.find('h3', class_='arc-title').text.strip()
        
        # 提取所有內容
        content = soup.find('div', class_='blogbody').get_text()
        
        # 分段處理各部分
        sections = {}
        current_section = None
        current_text = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # 判斷段落開始
            if line.startswith('《') and line.endswith('》：'):
                if current_section and current_text:
                    sections[current_section] = '\n'.join(current_text)
                current_section = line[1:-2]  # 移除《》：
                current_text = []
            elif current_section:
                current_text.append(line)
        
        # 處理最後一個段落
        if current_section and current_text:
            sections[current_section] = '\n'.join(current_text)
            
        # 處理占解部分
        divination = {}
        if '占解' in sections:
            div_text = sections['占解']
            for line in div_text.split('\n'):
                if '：' in line:
                    parts = [p.strip() for p in line.split('　　')]
                    for part in parts:
                        if '：' in part:
                            key, value = part.split('：', 1)
                            divination[key.strip()] = [v.strip() for v in value.split('、')]
        
        # 處理字詞說明
        notes = {}
        if sections.get('白沙屯媽祖婆網站字解'):
            for line in sections['白沙屯媽祖婆網站字解'].split('\n'):
                if '：' in line:
                    key, value = line.split('：', 1)
                    notes[key.strip()] = value.strip()

        return {
            "籤號": title,
            "籤詩": sections.get('籤詩', '').split('\n'),
            "籤意淺釋": sections.get('籤意淺釋', ''),
            "占解": divination,
            "字詞說明": notes,
            "說明": sections.get('說明', '')
        }

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None


def get_image(url,name):
    img_res = requests.get(url)
    filename = f'{name}.jpg'
    with open(filename, 'wb') as f:
        f.write(img_res.content)
    


def main():
    for i in range(1,101):
        get_image(f'https://www.baishatun.com.tw/31/101/{i}.JPG',str(i))
        print(f'{i} done')



    # 檢查檔案是否存在，不存在則創建
    # try:
    #     with open('fortunes.json', 'r', encoding='utf-8') as f:
    #         try:
    #             existing_data = json.load(f)
    #             # 確保是字典格式
    #             if isinstance(existing_data, str):
    #                 existing_data = json.loads(existing_data)
    #         except json.JSONDecodeError:
    #             # 如果檔案存在但不是有效的JSON
    #             existing_data = {}
    # except FileNotFoundError:
    #     # 如果檔案不存在，創建空字典
    #     existing_data = {}
    #     with open('fortunes.json', 'w', encoding='utf-8') as f:
    #         json.dump({}, f, ensure_ascii=False, indent=2)
    #     print("Created new fortunes.json file")
    
    # url = "https://www.mstn.org/168/?p=310"
    # fortune = get_fortune(url)
    # print(fortune)
   


if __name__ == "__main__":
    main()