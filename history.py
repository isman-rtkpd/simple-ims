import items
import db_helper

def add_history(entry_type, entry_id, prev_value, new_value, notes):
    parsed_req = [entry_type, entry_id, prev_value, new_value, notes]
    db_helper.history_db_insert(parsed_req)
