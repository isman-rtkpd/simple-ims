import locale

def format_number(text, with_prefix=False, decimal=0):
    try:
        text = int(text)
    except:
        return text
    if 'id_id' in locale.locale_alias:
        try:
            locale.setlocale(locale.LC_NUMERIC, 'id_id')
        except:
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

