import items
import db_helper

def add_history(entry_type, entry_id, prev_value, new_value, notes):
    parsed_req = [entry_type, entry_id, prev_value, new_value, notes]
    db_helper.history_db_insert(parsed_req)


def get_history_as_html():
    raw_db_data = db_helper.history_db_read()
    item_dict = db_helper.items_db_get_kv()
    package_dict = db_helper.packages_db_get_kv()
    
    print(item_dict)
    print(package_dict)
    
    
    html = ""
    for db_data in raw_db_data:
        entry_type = db_data[1]

        html += "<tr>"    
        html += "<td>%s</td>" % db_data[0] 
        html += "<td>%s</td>" % entry_type
        if entry_type == "item":
            html += "<td>%s</td>" % item_dict[int(db_data[2])]
        elif entry_type == "package":
            html += "<td>%s</td>" % package_dict[int(db_data[2])]
            
        html += "<td hidden>%s</td>" % db_data[3] 
        html += "<td hidden>%s</td>" % db_data[4] 
        html += "<td>%s</td>" % db_data[5] 
        html += "</tr>"
    return html
    