import db_helper
import items
from datetime import datetime
import history
import json
import util

def read_from_db():
    raw_data = db_helper.packages_db_read(None)
    return raw_data

def parse_db_data_to_html(raw_db_data):
    html = ""
    
    for db_data in raw_db_data:
        modal_price = items.calculate_modal_price(db_data[0])
        selected_item = [int(x) for x in db_data[5].split(',')]
        
        parsed_associated_items, code = items.parse_associated_items(selected_item)
        item_stock_kv = db_helper.items_db_get_kv_stock()
        
        if code == "ORANGE":
            html += '<tr bgcolor="orange" style="color:white;">'   
        elif code == "RED":
            html += '<tr bgcolor="darkred" style="color:white;">'        
        else:
            html += "<tr>"
            
        html += "<td>%s</td>" % db_data[0] #package id
        html += "<td style=\"text-align: center;\">%s</td>" % db_data[2] #package name
        html += "<td style=\"text-align: right;\">%s</td>" % util.format_number(db_data[3]) #sold number
        html += "<td style=\"text-align: right;\">%s</td>" % util.format_number(modal_price, True)  #modal price
        html += "<td style=\"text-align: right;\">%s</td>" % util.format_number(db_data[4], True) #selling price
        html += "<td style=\"text-align: right;\">%s</td>" % util.format_number((int(db_data[4]) - modal_price), True)               #margin
        
        min_stock_list = []
        for item in selected_item:
            min_stock_list.append(int(item_stock_kv[item]))
        else:
            min_stock = min(min_stock_list)
        
        html += "<td style=\"text-align: right;\">%s</td>" % util.format_number(min_stock) #associated items
        html += "<td>%s</td>" % parsed_associated_items #associated items
        html += '<td><a href="/packages/add/%s"><button class="button-action">Edit</button></a></td>' % db_data[0]
        html += "</tr>"
    return html

def deduct_package(package_id, qty):
    raw_package_data = db_helper.packages_db_read(package_id)[0]
    related_items = [int(x) for x in raw_package_data[5].split(',')]
    for item_id in related_items:
        items.deduct_item(item_id, qty, "Sold")
    sold_number = int(raw_package_data[3])
    
    print("RAWWW %s" % raw_package_data[3])
    new_sold_number = int(sold_number) + int(qty)
    db_helper.packages_db_update(package_id, "sold_number", str(new_sold_number))
    history.add_history("package", str(package_id), json.dumps(raw_package_data[1:]), json.dumps(list(raw_package_data[1:3]) + [new_sold_number] + list(raw_package_data[4:])), str(-1 * qty), "Sold")


def add_to_db(form_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    package_name = form_data['package_name']
    package_selling_price = form_data['package_selling_price']
    checked = []
    checked_items = list(form_data.keys())
    for item in checked_items:
        if "item_" in item: checked.append(item.split("item_")[1])
    checked_string = ",".join(checked)
    req = [timestamp, package_name, package_selling_price, checked_string]
    last_row_id = db_helper.packages_db_insert(req)
    history.add_history("package", str(last_row_id), json.dumps([]), json.dumps(req + [0]), "0", "Added new package")
    
def update_values(package_id, form_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    package_name = form_data['package_name']
    package_selling_price = form_data['package_selling_price']
    old_data = db_helper.packages_db_read(package_id)[0]
    checked = []
    checked_items = list(form_data.keys())
    for item in checked_items:
        if "item_" in item: checked.append(item.split("item_")[1])
    checked_string = ",".join(checked)
    
    db_helper.packages_db_update(package_id, "updated_date", timestamp)
    db_helper.packages_db_update(package_id, "package_name", package_name)
    db_helper.packages_db_update(package_id, "selling_price", package_selling_price)
    db_helper.packages_db_update(package_id, "related_item", checked_string)
    history.add_history("package", str(package_id), json.dumps(old_data[1:]), json.dumps([timestamp, package_name, package_selling_price, checked_string, old_data[-1]]), str(old_data[3]),  "Update package")
