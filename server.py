from flask import Flask, request, jsonify, render_template, make_response, send_from_directory,redirect

import db_helper
import items
import packages

app = Flask(__name__)

@app.route("/")
def main_page():
    stock_notification = items.check_for_below_threshold()
    
    return render_template("index.html", notification = stock_notification)

@app.route("/items/list")
def items_list():
    item_data_db = items.read_from_db()
    html = items.parse_db_data_to_html(item_data_db)
    return render_template("items/list.html", item_data = html)

@app.route("/items/add/<index>")
def items_add_get(index):
    if index == "0":
        return render_template("items/add.html", db_notify = "no", action = "Add new item")
    else:
        db_data = db_helper.items_db_read(index)[0]
        return render_template("items/add.html", db_name = db_data[2], db_qty = db_data[3], db_modal = db_data[4], db_selling = db_data[5], db_notify = db_data[6], db_notify_thres = db_data[7], action = "Edit item. ID: %s" % index)

@app.route("/items/add/<index>", methods=["POST"])
def items_add_post(index):
    if index == "0":
        items.add_to_db(request.form)        
    else:
        items.update_values(index, request.form)
    return redirect("/items/list")


@app.route("/packages/list")
def packages_list():
    package_data_db = packages.read_from_db()
    html = packages.parse_db_data_to_html(package_data_db)
    return render_template("packages/list.html", package_data = html)

@app.route("/packages/add/<index>")
def packages_add_get(index):
    if index == "0":
        item_list_html = items.populate_items_html_for_package(None)
        return render_template("packages/add.html", populated_items = item_list_html, action = "Add new package")
    else:
        db_data = db_helper.packages_db_read(index)[0]
        item_list_html = items.populate_items_html_for_package(index)
        return render_template("packages/add.html", populated_items = item_list_html, db_name = db_data[2], db_selling = db_data[4], action = "Edit Package. ID: %s" % index)

@app.route("/packages/add/<index>", methods=["POST"])
def packages_add_post(index):
    print(request.form)
    if index == "0":
        packages.add_to_db(request.form)        
    else:
        packages.update_values(index, request.form)
    return redirect("/packages/list")


if __name__ == "__main__":
    # Run this web app in debug mode
    # The debug mode can detect the code changes of the server module, and automatically restart the service if there is any modification
    db_helper.items_db_setup()
    db_helper.packages_db_setup()
    app.run(host="0.0.0.0", port=8080, debug=True)