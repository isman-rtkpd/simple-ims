import db_helper
import history
from datetime import datetime
import json

def read_from_db():
    raw_data = db_helper.items_db_read(None)
    return raw_data

def parse_db_data_to_html(raw_db_data):
    html = ""
    
    for db_data in raw_db_data:
        
        if int(db_data[3]) < int(db_data[7]):
            html_head = '<tr bgcolor="orange" style="color:white;">'   
            if int(db_data[3]) <= 0:
                html_head = '<tr bgcolor="darkred" style="color:white;">'        
        else:
            html_head = "<tr>"
        html += html_head
        html += "<td>%s</td>" % db_data[0]
        html += "<td>%s</td>" % db_data[2]
        html += "<td>%s</td>" % db_data[3]
        html += "<td>%s</td>" % db_data[5]        
        html += "<td>%s</td>" % (int(db_data[5]) - int(db_data[4]))
        html += "<td>%s</td>" % int(db_data[8])
        html += "<td>%s</td>" % db_data[4]   
        html += '<td><a href="/items/add/%s"><button class="button-action">Edit</button></a></td>' % db_data[0]
        html += "</tr>"
        
    return html

def deduct_item(item_id, qty, from_package = None):
    old_val = db_helper.items_db_read(item_id)[0]
    cur_qty = int(db_helper.items_db_read(item_id)[0][3])
    new_qty = cur_qty - qty
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_helper.items_db_update(item_id, "quantity", new_qty)
    db_helper.items_db_update(item_id, "updated_date", timestamp)
    sold_number = old_val[8]
    msg = ""
    if from_package == None:
        if qty < 0:
            msg = "%s quantity as incoming stock" % (int(qty) * -1)
        else:
            msg = "%s quantity as outgoing stock" % qty
            db_helper.items_db_update(item_id, "sold_number", int(sold_number) + int(qty))
    else:
        msg = from_package

    
    new_val = [timestamp] + [old_val[2]] + [str(new_qty)] + list(old_val[4:])
    history.add_history("item", item_id, json.dumps(old_val[1:]), json.dumps(new_val), msg)
    

def add_to_db(form_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_name = form_data['item_name']
    item_modal_price = form_data['item_modal_price']
    item_selling_price = form_data['item_selling_price']
    item_qty = form_data['item_quantity']
    item_notify = form_data['notify_options']
    item_notify_threshold = form_data['notify_threshold']
    req = [timestamp, item_name, item_qty, item_modal_price, item_selling_price, item_notify, item_notify_threshold]
    last_row_id = db_helper.items_db_insert(req)
    history.add_history("item", str(last_row_id), json.dumps([]), json.dumps(req + [0]), "Added new item")
    
    
def update_values(item_id, form_data):
    old_val = json.dumps(db_helper.items_db_read(item_id)[0][1:])
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_name = form_data['item_name']
    item_modal_price = form_data['item_modal_price']
    item_selling_price = form_data['item_selling_price']
    item_qty = form_data['item_quantity']
    item_notify = form_data['notify_options']
    if item_notify == "no":
        item_notify_threshold = "1"
    else:
        item_notify_threshold = form_data['notify_threshold']
        
    new_val = json.dumps([timestamp, item_name, item_qty, item_modal_price, item_selling_price, item_notify, item_notify_threshold, old_val[8]])
    db_helper.items_db_update(item_id, "updated_date", timestamp)
    db_helper.items_db_update(item_id, "item_name", item_name)
    db_helper.items_db_update(item_id, "quantity", item_qty)
    db_helper.items_db_update(item_id, "modal_price", item_modal_price)
    db_helper.items_db_update(item_id, "selling_price", item_selling_price)
    db_helper.items_db_update(item_id, "notify_stock", item_notify)
    db_helper.items_db_update(item_id, "notify_thres", item_notify_threshold)
    history.add_history("item", item_id, old_val, new_val, "Update item attribute")
    
def populate_items_html_for_package(package_id):
    raw_db_data = read_from_db()
    html = ""
    code = ""
    if package_id == None or package_id == 0:
        html += ""
        for db_data in raw_db_data:
            style = ""
            if int(db_data[3]) < int(db_data[7]):
                style = 'style="color:orange;"'
                if int(db_data[3]) <= 0:
                    style = 'style="color:darkred;"'
            html += '<input type="checkbox" id="item_%s" name="item_%s" value="%s"><label for="item_%s" %s> %s</label><br>' %  (db_data[0], db_data[0], db_data[2], db_data[0], style, db_data[2])
        return html, code
    else:
        index = 1
        package_data = [int(x) for x in db_helper.packages_db_read(package_id)[0][5].split(',')]
        code = ""
        for db_data in raw_db_data:
            if index in package_data:
                checked = "checked"
                print("checked")
                if int(db_data[3]) < int(db_data[7]) and code != "RED":
                    code = "ORANGE"
                    if int(db_data[3]) <= 0:
                        code = "RED"
            else:
                checked = ""
            
            style = ""
            if int(db_data[3]) < int(db_data[7]):
                style = 'style="color:orange;"'
                if int(db_data[3]) <= 0:
                    style = 'style="color:darkred;"'
            html += '<input type="checkbox" id="item_%s" name="item_%s" value="%s" %s><label for="item_%s" %s> %s</label><br>' % (db_data[0], db_data[0], db_data[2], checked, db_data[0], style, db_data[2])
            index += 1
        print(code)
        return html, code
    
def check_for_below_threshold():
    #notify
    raw_db_data = read_from_db()
    html = ""
    
    for db_data in raw_db_data:
        if (db_data[6] == "yes" and int(db_data[3]) < int(db_data[7])) or (int(db_data[3]) <= 0):

            if int(db_data[3]) <= 0:
                html += '<tr bgcolor="darkred" style="color:white;">'
            else:
                html += '<tr bgcolor="orange" style="color:white;">'            
            html += '<td>%s</a></td>' % db_data[2]
            
            if db_data[6] == "yes":
                html += '<td>%s</td>' % db_data[7]
            else:
                html += '<td>--</td>'

            html += '<td>%s</td>' % db_data[3]    
            html += '<td><a href="/items/add/%s"><button class="button-action">Edit</button></a></td>' % db_data[0]
            html += '</tr>' 
    
    return html
    
def calculate_modal_price(package_id):
    index = 1
    total = 0
    raw_db_data = read_from_db()
    package_data = [int(x) for x in db_helper.packages_db_read(package_id)[0][5].split(',')]
    for db_data in raw_db_data:
        if index in package_data:
            total += int(db_data[4])
        index += 1
    return total


def parse_associated_items(package_id):
    code = "" # ORANGE -> have item below threshold, RED -> have 0 stock
    index = 1
    items = []
    raw_db_data = read_from_db()
    package_data = [int(x) for x in db_helper.packages_db_read(package_id)[0][5].split(',')]
    for db_data in raw_db_data:
        if index in package_data:
            items.append(db_data[2])
            if int(db_data[3]) < int(db_data[7]):
                code = "ORANGE"
                if int(db_data[3]) <= 0:
                    code = "RED"
        index += 1
    output = ''
    for item_name in items:
        output += "<li>%s</li>" % item_name
    
    output = "<ul>%s</ul>" % output
    
    return output, code