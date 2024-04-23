import items
import db_helper
from datetime import datetime

def add_history(entry_type, entry_id, prev_value, new_value, notes):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parsed_req = [entry_type, entry_id, prev_value, new_value, notes, timestamp]
    db_helper.history_db_insert(parsed_req)


def get_history_as_html():
    raw_db_data = db_helper.history_db_read()
    item_dict = db_helper.items_db_get_kv()
    package_dict = db_helper.packages_db_get_kv()    
    
    html = ""
    for db_data in raw_db_data:
        entry_type = db_data[1]

        html += "<tr>"    
        html += "<td>%s</td>" % db_data[0]
        html += "<td>%s</td>" % db_data[6] 
        html += "<td>%s</td>" % entry_type
        if entry_type == "item":
            html += "<td>%s</td>" % item_dict[int(db_data[2])]
        elif entry_type == "package":
            html += "<td>%s</td>" % package_dict[int(db_data[2])]
            
        html += "<td hidden>%s</td>" % db_data[3] 
        html += "<td hidden>%s</td>" % db_data[4] 
        html += "<td>%s</td>" % db_data[5] 
        html += '<td><a href="/history/detail/%s"><button class="button-action">detail</button></a></td>' % db_data[0]
        html += "</tr>"
    return html
    