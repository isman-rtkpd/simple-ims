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
    c.execute(statement)
    
    conn.commit()
    conn.close()
    
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