import db_helper
from datetime import datetime

def read_from_db():
    raw_data = db_helper.packages_db_read(None)
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
        html += '<td><a href="/packages/add/%s">Edit</a></td>' % db_data[0]
        html += "</tr>"
    return html

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
    package_items = form_data['items_options']
    db_helper.packages_db_update(package_id, "updated_date", timestamp)
    db_helper.packages_db_update(package_id, "package_name", package_name)
    db_helper.packages_db_update(package_id, "selling_price", package_selling_price)
    db_helper.packages_db_update(package_id, "related_item", package_items)
