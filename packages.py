import db_helper
import items
from datetime import datetime

def read_from_db():
    raw_data = db_helper.packages_db_read(None)
    return raw_data

def parse_db_data_to_html(raw_db_data):
    html = ""
    
    for db_data in raw_db_data:
        modal_price = items.calculate_modal_price(db_data[0])
        parsed_associated_items, code = items.parse_associated_items(db_data[0])
        
        if code == "ORANGE":
            html += '<tr bgcolor="orange" style="color:white;">'   
        elif code == "RED":
            html += '<tr bgcolor="darkred" style="color:white;">'        
        else:
            html += "<tr>"
            
        html += "<td>%s</td>" % db_data[0] #package id
        html += "<td>%s</td>" % db_data[2] #package name
        html += "<td>%s</td>" % db_data[3] #sold number
        html += "<td>%s</td>" % modal_price  #modal price
        html += "<td>%s</td>" % db_data[4] #selling price
        html += "<td>%s</td>" % (int(db_data[4]) - modal_price)               #margin
        html += "<td>%s</td>" % parsed_associated_items #associated items
        html += '<td><a href="/packages/add/%s"><button>Edit</button></a></td>' % db_data[0]
        html += "</tr>"
    return html

def deduct_package(package_id, qty):
    related_items = [int(x) for x in db_helper.packages_db_read(package_id)[0][5].split(',')]
    for item_id in related_items:
        items.deduct_item(item_id, qty)

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
    db_helper.packages_db_insert(req)
    
def update_values(package_id, form_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    package_name = form_data['package_name']
    package_selling_price = form_data['package_selling_price']
    
    checked = []
    checked_items = list(form_data.keys())
    for item in checked_items:
        if "item_" in item: checked.append(item.split("item_")[1])
    checked_string = ",".join(checked)
    
    db_helper.packages_db_update(package_id, "updated_date", timestamp)
    db_helper.packages_db_update(package_id, "package_name", package_name)
    db_helper.packages_db_update(package_id, "selling_price", package_selling_price)
    db_helper.packages_db_update(package_id, "related_item", checked_string)
