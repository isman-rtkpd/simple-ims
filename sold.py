import items
import db_helper
import util

def parse_packages_db_data(raw_db_data):
    html = ""
    for db_data in raw_db_data:
        _, code = items.populate_items_html_for_package(db_data[0])
        if code == "ORANGE":
            html += '<tr bgcolor="orange" style="color:white;">'
        elif code == "RED":
            html += '<tr bgcolor="darkred" style="color:white;">'
        else:
            html += "<tr>"
            
        
        selected_item = [int(x) for x in db_data[5].split(',')]
        item_stock_kv = db_helper.items_db_get_kv_stock()        
        min_stock_list = []
        for item in selected_item:
            min_stock_list.append(int(item_stock_kv[item]))
        else:
            min_stock = min(min_stock_list)
        
        html += "<td>%s</td>" % db_data[0] #package id
        html += '<td style=\"text-align: left;\">%s</td>' % (db_data[2]) #package name
        html += "<td style=\"text-align: right;\">%s</td>" % util.format_number(min_stock) #availstock

        html += '<td><input type="number" id="sold_package_%s" placeholder="0" min="1" required></td>' % db_data[0]
        html += '<td><button onclick="soldPackage(%s);" class="button-action">Adjust</button></td>' % (db_data[0])
        html += '<td><a href="/packages/add/%s"><button class="button-action">Edit package</button></a></td>' % (db_data[0])
        html += "</tr>"
    return html

def parse_items_db_data(raw_db_data):
    html = ""
    
    for db_data in raw_db_data:
        style = ''
        if int(db_data[3]) < int(db_data[7]):
            style = 'bgcolor="orange" style="color:white;"'
            if int(db_data[3]) <= 0:
                style = 'bgcolor="darkred" style="color:white;"'
        
        html += "<tr %s>" % style
        html += "<td>%s</td>" % db_data[0]
        html += "<td style=\"text-align: left;\">%s</td>" % db_data[2]
        html += "<td style=\"text-align: right;\">%s</td>" % util.format_number(db_data[3])
        html += '<td><input type="number" id="sold_item_%s" placeholder="0" required></td>' % db_data[0]
        html += '<td><button onclick="soldItem(%s);" class="button-action">Adjust</button></td>' % (db_data[0])
        html += '<td><a href="/items/add/%s"><button class="button-action">Edit item</button></a></td>' % (db_data[0])
        html += "</tr>"
    return html