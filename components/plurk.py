from plurk_oauth import PlurkAPI
from dotenv import load_dotenv
import os
load_dotenv()
CONSUMER_KEY=os.getenv('plurk_App_key')
CONSUMER_SECRET= os.getenv('plurk_App_secret')
ACCESS_TOKEN= os.getenv('plurk_token')
ACCESS_TOKEN_SECRET=os.getenv('plurk_secret')

plurk = PlurkAPI(CONSUMER_KEY, CONSUMER_SECRET)
plurk.authorize(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# imagestore = plurk.callAPI('/APP/Photos/list',{"offset":"0","limit":"1"})

def plurktest():
    saved = {'success_text': 'ok', 'photos': [
        {'user_id': 6634425, 'filename': '5or5xgnYvGn7fMBbVQVzyn.jpg', 'thumbnail': 'mx_5or5xgnYvGn7fMBbVQVzyn.jpg',
         'filetype': 'jpg', 'checksum': 'b13c0f517536c8ff2a561db55c59b577', 'orig_width': 387, 'orig_height': 280,
         'orig_size': 16667, 'status': 1, 'privacy': 0, 'plurk_id': 348756189077988, 'response_id': 630231302814037,
         'timeline_id': None, 'note': '', 'ordering': None, 'uploaded': 'Wed, 27 Mar 2024 15:52:20 GMT',
         'permalink': 'https://www.plurk.com/p/3fmgdqcxd0?r=630231302814037'}]}
    img = 'https://images.plurk.com/'+ saved['photos'][0]['filename']
    return img
