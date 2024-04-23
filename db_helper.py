import sqlite3
from datetime import datetime
import json
import os

CWD = os.getcwd()
DB_FOLDER = "db"

ITEMS_DB_NAME = "items.db"

ITEMS_DB_PATH = "%s/%s/%s" % (CWD, DB_FOLDER, ITEMS_DB_NAME)

def items_db_setup():
    '''Initialize items DB'''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
    
    statement = '''
        CREATE TABLE IF NOT EXISTS items(
            [item_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
            [updated_date] TEXT,
            [item_name] TEXT,
            [quantity] TEXT,
            [modal_price] TEXT,
            [selling_price] TEXT,
            [notify_stock] TEXT,
            [notify_thres] TEXT,
            [sold_number] TEXT
            )'''
    c.execute(statement)
                        
    conn.commit()
    conn.close()
    
def items_db_insert(parsed_request):
    '''Insert entry to items DB
    
    Parameters
    ----------
    parsed_request
        list of values
            [updated_date] TEXT,
            [item_name] TEXT,
            [quantity] TEXT,
            [modal_price] TEXT,
            [selling_price] TEXT,
            [notify_stock] TEXT,
            [notify_thres] TEXT
    Return:
    ----------
    void
        
    '''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
                    
    statement = "INSERT INTO items(updated_date, item_name, quantity, modal_price, selling_price, notify_stock, notify_thres, sold_number) VALUES (" + \
            "'%s', " % parsed_request[0] + \
            "'%s', " % parsed_request[1] + \
            "'%s', " % parsed_request[2] + \
            "'%s', " % parsed_request[3] + \
            "'%s', " % parsed_request[4] + \
            "'%s', " % parsed_request[5] + \
            "'%s', " % parsed_request[6] + \
            "'0')"
    res = c.execute(statement)
    
    conn.commit()
    conn.close()
    return res.lastrowid
    
def items_db_update(item_id, column, new_data):
    '''Update item value by item_id on column, update to new_data
        
    '''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
    
    statement = "UPDATE items set %s = '%s' where item_id = %s" % (column, new_data, item_id)
    c.execute(statement)
    
    conn.commit()
    conn.close()
    
def items_db_read(item_id = None):
    '''Get item data by item_id
    
    Parameters
    ----------
    item_id
    
    Return:
    ----------
    list
        list of values
        
    '''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
                    
    #Get latest index (to get last ticket id)
    if item_id == None:
        statement = 'SELECT * FROM items;'
    else:
        statement = 'SELECT * FROM items where item_id=%s;' % item_id
        
    c.execute(statement)
    output = c.fetchall()
    conn.close()
    return output

def items_db_get_kv():
    item_dict = dict()
    items = items_db_read()
    for item in items:
        item_dict[item[0]] = item[2]
    return item_dict

##########

def packages_db_setup():
    '''Initialize items DB'''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
    
    statement = '''
        CREATE TABLE IF NOT EXISTS packages(
            [package_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
            [updated_date] TEXT,
            [package_name] TEXT,
            [sold_number] TEXT,
            [selling_price] TEXT,
            [related_item] TEXT
            )'''
    c.execute(statement)
                        
    conn.commit()
    conn.close()
    
def packages_db_insert(parsed_request):
    '''Insert entry to items DB
    
    Parameters
    ----------
    parsed_request
        list of values
            [updated_date] TEXT,
            [package_name] TEXT,
            [selling_price] TEXT,
            [related_item] TEXT
    Return:
    ----------
    void
        
    '''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
                    
    statement = "INSERT INTO packages(updated_date, package_name, sold_number, selling_price, related_item) VALUES (" + \
            "'%s', " % parsed_request[0] + \
            "'%s', " % parsed_request[1] + \
            "'0' , " + \
            "'%s', " % parsed_request[2] + \
            "'%s');" % parsed_request[3]
    res = c.execute(statement)
    
    conn.commit()
    conn.close()
    return res.lastrowid
    
def packages_db_update(package_id, column, new_data):
    '''Update item value by item_id on column, update to new_data
        
    '''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
    
    statement = "UPDATE packages set %s = '%s' where package_id = %s" % (column, new_data, package_id)
    c.execute(statement)
    
    conn.commit()
    conn.close()
    
def packages_db_read(package_id = None):
    '''Get item data by item_id
    
    Parameters
    ----------
    item_id
    
    Return:
    ----------
    list
        list of values
        
    '''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
                    
    #Get latest index (to get last ticket id)
    if package_id == None:
        statement = 'SELECT * FROM packages;'
    else:
        statement = 'SELECT * FROM packages where package_id=%s;' % package_id
        
    c.execute(statement)
    
    output = c.fetchall()
    conn.close()
    return output

def packages_db_get_kv():
    package_dict = dict()
    packages = packages_db_read()
    for package in packages:
        package_dict[package[0]] = package[2]
    return package_dict


##########

def history_db_setup():
    '''Initialize items DB'''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
    
    statement = '''
        CREATE TABLE IF NOT EXISTS history(
            [history_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
            [entry_type] TEXT,
            [entry_id] TEXT,
            [prev_value] TEXT,
            [new_value] TEXT,
            [notes] TEXT
            )'''
    c.execute(statement)
                        
    conn.commit()
    conn.close()
    
def history_db_insert(parsed_request):
    '''Insert entry to history DB
    
    Parameters
    ----------
    parsed_request
        list of values
            [entry_type] TEXT, (ITEM, PACKAGE)
            [entry_id] TEXT, (ITEM_ID, ITEM_PACKAGE)
            [prev_value] TEXT,
            [new_value] TEXT,
            [notes] TEXT
    Return:
    ----------
    void
        
    '''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
                    
    print(parsed_request)
    statement = "INSERT INTO history(entry_type, entry_id, prev_value, new_value, notes) VALUES (" + \
            "'%s', " % parsed_request[0] + \
            "'%s', " % parsed_request[1] + \
            "'%s', " % parsed_request[2] + \
            "'%s', " % parsed_request[3] + \
            "'%s');" % parsed_request[4]
            
    print("STATEMENT:" + str(statement))
    c.execute(statement)
    
    conn.commit()
    conn.close()
    
    
def history_db_read():
    '''
        
    Return:
    ----------
    list
        list of values
        
    '''
    conn = sqlite3.connect(ITEMS_DB_PATH) 
    c = conn.cursor()
                    
    #Get latest index (to get last ticket id)
    statement = 'SELECT * FROM history;'
        
    c.execute(statement)
    
    output = c.fetchall()
    conn.close()
    return output
