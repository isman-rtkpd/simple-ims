def parse_packages_db_data(raw_db_data):
    html = ""
    for db_data in raw_db_data:
        html += "<tr>"
        html += "<td>%s</td>" % db_data[0] #package name
        html += '<td><a href="/packages/add/%s">%s</a></td>' % (db_data[0], db_data[2]) #package id
        html += '<td><input type="number" id="sold_package_%s" placeholder="0" min="1" required></td>' % db_data[0]
        html += '<td><button onclick="soldPackage(%s);">Adjust</button></td>' % (db_data[0])
        html += "</tr>"
    return html

def parse_items_db_data(raw_db_data):
    html = ""
    
    for db_data in raw_db_data:
        html += "<tr>"
        html += "<td>%s</td>" % db_data[0]
        html += "<td>%s</td>" % db_data[2]
        html += "<td>%s</td>" % db_data[3]
        html += '<td><input type="number" id="sold_item_%s" placeholder="0" min="1" required></td>' % db_data[0]
        html += '<td><button onclick="soldItem(%s);">Adjust</button></td>' % (db_data[0])
        html += "</tr>"
    return html