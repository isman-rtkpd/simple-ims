import locale

available_locales = []
for l in locale.locale_alias:
    try:
        locale.setlocale(locale.LC_ALL, l)
        available_locales.append(l)
    except:
        pass

def format_number(text, with_prefix=False, decimal=0):
    text = int(text)
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

