from flask import Flask, request, jsonify, render_template, make_response, send_from_directory,redirect

import db_helper
import items

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/items/list")
def items_list():
    item_data_db = items.read_from_db()
    html = items.parse_db_data_to_html(item_data_db)
    return render_template("items/list.html", item_data = html)

@app.route("/items/add/<index>")
def items_add_get(index):
    if index == "0":
        return render_template("items/add.html", db_notify = "no")
    else:
        db_data = db_helper.items_db_read(index)[0]
        return render_template("items/add.html", db_name = db_data[2], db_qty = db_data[3], db_modal = db_data[4], db_selling = db_data[5], db_notify = db_data[6], db_notify_thres = db_data[7])

@app.route("/items/add/<index>", methods=["POST"])
def items_add_post(index):
    if index == "0":
        items.add_to_db(request.form)        
    else:
        items.update_values(index, request.form)
    return redirect("/items/list")

if __name__ == "__main__":
    # Run this web app in debug mode
    # The debug mode can detect the code changes of the server module, and automatically restart the service if there is any modification
    db_helper.items_db_setup()
    app.run(host="0.0.0.0", port=8080, debug=True)