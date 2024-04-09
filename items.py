import db_helper
from datetime import datetime

def read_from_db():
    raw_data = db_helper.items_db_read(None)
    return raw_data

def parse_db_data_to_html(raw_db_data):
    html = ""
    
    for db_data in raw_db_data:
        html += "<tr>"
        html += "<td>%s</td>" % db_data[0]
        html += "<td>%s</td>" % db_data[2]
        html += "<td>%s</td>" % db_data[3]
        html += "<td>%s</td>" % db_data[4]   
        html += "<td>%s</td>" % db_data[5]        
        html += "<td>%s</td>" % (int(db_data[5]) - int(db_data[4]))
        html += "<td>%s</td>" % int(db_data[8])
        html += '<td><a href="/items/add/%s">Edit</a></td>' % db_data[0]
        html += "</tr>"
    return html

def add_to_db(form_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_name = form_data['item_name']
    item_modal_price = form_data['item_modal_price']
    item_selling_price = form_data['item_selling_price']
    item_qty = form_data['item_quantity']
    item_notify = form_data['notify_options']
    item_notify_threshold = form_data['notify_threshold']
    req = [timestamp, item_name, item_qty, item_modal_price, item_selling_price, item_notify, item_notify_threshold]
    db_helper.items_db_insert(req)
    
def update_values(item_id, form_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_name = form_data['item_name']
    item_modal_price = form_data['item_modal_price']
    item_selling_price = form_data['item_selling_price']
    item_qty = form_data['item_quantity']
    item_notify = form_data['notify_options']
    item_notify_threshold = form_data['notify_threshold']
    db_helper.items_db_update(item_id, "updated_date", timestamp)
    db_helper.items_db_update(item_id, "item_name", item_name)
    db_helper.items_db_update(item_id, "quantity", item_qty)
    db_helper.items_db_update(item_id, "modal_price", item_modal_price)
    db_helper.items_db_update(item_id, "selling_price", item_selling_price)
    db_helper.items_db_update(item_id, "notify_stock", item_notify)
    db_helper.items_db_update(item_id, "notify_thres", item_notify_threshold)
    
def populate_items_html_for_package(package_id):
    raw_db_data = read_from_db()
    html = ""
    
    if package_id == None or package_id == 0:
        for db_data in raw_db_data:
            html += '<input type="checkbox" id="item_%s" name="item_%s" value="%s" ><label for="item_%s"> %s</label><br>' % (db_data[0], db_data[0], db_data[2], db_data[0], db_data[2])        
        return html
    else:
        index = 1
        package_data = [int(x) for x in db_helper.packages_db_read(package_id)[0][5].split(',')]
        for db_data in raw_db_data:
            if index in package_data:
                html += '<input type="checkbox" id="item_%s" name="item_%s" value="%s" checked><label for="item_%s"> %s</label><br>' % (db_data[0], db_data[0], db_data[2], db_data[0], db_data[2])
            else:
                html += '<input type="checkbox" id="item_%s" name="item_%s" value="%s"><label for="item_%s"> %s</label><br>' % (db_data[0], db_data[0], db_data[2], db_data[0], db_data[2])
            index += 1
        return html