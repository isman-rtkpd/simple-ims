import items
import db_helper
from datetime import datetime
import util

def add_history(entry_type, entry_id, prev_value, new_value, diff, notes):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parsed_req = [entry_type, entry_id, prev_value, new_value, diff, notes, timestamp]
    db_helper.history_db_insert(parsed_req)


def get_history_as_html(limit = 50, page = 1):
    raw_db_data = db_helper.history_db_read(limit, page)
    item_dict = db_helper.items_db_get_kv()
    package_dict = db_helper.packages_db_get_kv()    
    
    html = ""
    for db_data in raw_db_data:
        entry_type = db_data[1]

        html += "<tr>"    
        html += "<td>%s</td>" % db_data[0]
        the_date = db_data[7]
        spl = the_date.split()[0].split("-")
        the_date_out = '-'.join([spl[2], spl[1], spl[0]]) + " " + str(the_date.split()[1]) 
        html += "<td>%s</td>" % the_date_out
        if entry_type == "item":
            html += "<td>%s</td>" % item_dict[int(db_data[2])]
        elif entry_type == "package":
            html += "<td>%s</td>" % package_dict[int(db_data[2])]
        html += "<td>%s</td>" % entry_type
        
        stock = ""
        if entry_type == "item":
            stock = db_data[5]
        elif entry_type == "package":
            if str(db_data[5]) == "0":
                 stock = "--"
            else:
                stock = db_data[5]
            
        html += "<td style=\"text-align: right;\">%s</td>" % util.format_number(stock)
        html += "<td hidden>%s</td>" % db_data[3] 
        html += "<td hidden>%s</td>" % db_data[4] 
        html += "<td>%s</td>" % db_data[6] 
        html += '<td><a href="/history/detail/%s"><button class="button-action">detail</button></a></td>' % db_data[0]
        html += "</tr>"
    return html
    
