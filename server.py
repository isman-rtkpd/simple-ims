from flask import Flask, request, jsonify, render_template, make_response, send_from_directory,redirect, abort

import db_helper
import items
import packages
import sold
import json
import history
import util
import const
from datetime import datetime
from time import sleep
import hashlib

app = Flask(__name__, static_url_path='/static')

#password is in const file
hash_password = const.PASSWORD

@app.route("/")
def main_page():
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        stock_notification = items.check_for_below_threshold()
        return render_template("index.html", notification = stock_notification)
    else:
        return render_template("auth.html")
    
@app.route("/", methods = ["POST"])
def page_authentication():
    val_password = request.form['password']
    if hashlib.sha256(val_password.encode()).hexdigest() == hash_password:        
        resp = make_response(redirect("/"))
        resp.set_cookie('password', hash_password) 
        resp.set_cookie('expiry', str(int(datetime.now().timestamp() + 24 * 3600)))
        return resp
    else:
        sleep(15)
        redirect("/")


@app.route("/items/list")
def items_list():
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        item_data_db = items.read_from_db()
        html = items.parse_db_data_to_html(item_data_db)
        return render_template("items/list.html", item_data = html)
    else:
        sleep(15)
        abort(404)


@app.route("/items/add/<index>")
def items_add_get(index):
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        if index == "0":
            return render_template("items/add.html", db_notify = "no", action = "Add new item")
        else:
            db_data = db_helper.items_db_read(index)[0]
            return render_template("items/add.html", db_name = db_data[2], db_qty = db_data[3], db_modal = db_data[4], db_selling = db_data[5], db_notify = db_data[6], db_notify_thres = db_data[7], action = "Edit item. ID: %s" % index)
    else:
        sleep(15)
        abort(404)

@app.route("/items/add/<index>", methods=["POST"])
def items_add_post(index):
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        if index == "0":
            items.add_to_db(request.form)        
        else:
            items.update_values(index, request.form)
        return redirect("/items/list")
    else:
        sleep(15)
        abort(404)

@app.route("/packages/list")
def packages_list():
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        package_data_db = packages.read_from_db()
        html = packages.parse_db_data_to_html(package_data_db)
        return render_template("packages/list.html", package_data = html)
    else:
        sleep(15)
        abort(404)

@app.route("/packages/add/<index>")
def packages_add_get(index):
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        if index == "0":
            item_list_html, _ = items.populate_items_html_for_package(None)
            return render_template("packages/add.html", populated_items = item_list_html, action = "Add new package")
        else:
            db_data = db_helper.packages_db_read(index)[0]
            item_list_html,_ = items.populate_items_html_for_package(index)
            return render_template("packages/add.html", populated_items = item_list_html, db_name = db_data[2], db_selling = db_data[4], action = "Edit Package. ID: %s" % index)
    else:
        sleep(15)
        abort(404)

@app.route("/packages/add/<index>", methods=["POST"])
def packages_add_post(index):
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        if index == "0":
            packages.add_to_db(request.form)        
        else:
            packages.update_values(index, request.form)
        return redirect("/packages/list")
    else:
        sleep(15)
        abort(404)

@app.route("/stockadjustment/list")
def stockadjustment_list():
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        package_data_db = packages.read_from_db()
        item_data_db = items.read_from_db()
        html_package_data = sold.parse_packages_db_data(package_data_db)
        html_item_data = sold.parse_items_db_data(item_data_db)
        html = packages.parse_db_data_to_html(package_data_db)
        return render_template("stockadjustment/list.html", package_data = html_package_data, item_data = html_item_data)
    else:
        sleep(15)
        abort(404)

@app.route("/stockadjustment/item/<itemid>", methods = ["POST"])
def stockadjustment_by_item(itemid):
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        qty = json.loads(request.data)['qty']
        items.deduct_item(itemid,int(qty))
        return make_response()
    else:
        sleep(15)
        abort(404)
        
@app.route("/stockadjustment/package/<packageid>", methods = ["POST"])
def stockadjustment_by_package(packageid):
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        qty = json.loads(request.data)['qty']
        packages.deduct_package(packageid, int(qty))
        return make_response()
    else:
        sleep(15)
        abort(404)

@app.route("/history/list", methods = ["GET"])
def get_history():
    valid_cookies = util.check_cookies(hash_password, request.cookies)
    if valid_cookies:
        html = history.get_history_as_html()
        return render_template("history/list.html", history_data = html)
    else:
        sleep(15)
        abort(404)

if __name__ == "__main__":
    # Run this web app in debug mode
    # The debug mode can detect the code changes of the server module, and automatically restart the service if there is any modification
    db_helper.items_db_setup()
    db_helper.packages_db_setup()
    db_helper.history_db_setup()
    app.run(host="0.0.0.0", port=8082, debug=True)
