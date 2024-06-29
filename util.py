import locale
from datetime import datetime
import requests
import const

def format_number(text, with_prefix=False, decimal=0):
    try:
        text = int(text)
    except:
        return text
    
    can_set_locale = False
    try:
        locale.setlocale(locale.LC_NUMERIC, 'id_id')
        can_set_locale = True
    except:
        pass
    
    if not can_set_locale:
        try:
            locale.setlocale(locale.LC_NUMERIC, 'id_ID')
            can_set_locale = True
        except:
            pass
        
    if not can_set_locale:
        locale.setlocale(locale.LC_NUMERIC, 'no_no')

    price = locale.format_string("%.*f", (decimal, text), True)
    if with_prefix:
        if text >= 0:    
            price = locale.format_string("%.*f", (decimal, text), True)
            return "IDR{}".format(price)
        else:    
            price = locale.format_string("%.*f", (decimal, -1*text), True)
            return "-IDR{}".format(price)
    return price

def check_cookies(hash_password, cookies):
    if hash_password == "":
        return True
    else:
        if cookies.get("password") == hash_password and int(datetime.now().timestamp()) < int(cookies.get("expiry")):
            return True
        else:
            return False
        
      
### START OF TELEGRAM  
def __telegram_command(name, data):
    url = const.TELEGRAM_API_URL(token=const.TELEGRAM_ACCESS_TOKEN, method=name)
    return requests.post(url=url, json=data)

def telegram_sendMessage(text: str, chat_id: str, notify=True):
    return __telegram_command('sendMessage', {
        'text': text,
        'chat_id': chat_id,
        'parse_mode': 'markdown',
        'disable_notification': not notify})
    
### END OF TELEGRAM