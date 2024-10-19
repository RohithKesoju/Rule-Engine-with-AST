import sqlite3
import json  # Use JSON to serialize/deserialize AST

def connect_db():
    conn = sqlite3.connect('rules.db')
    return conn

def save_rule(rule_string, ast):
    conn = connect_db()
    cursor = conn.cursor()
    # Serialize the AST to JSON format before saving
    ast_json = json.dumps(ast.to_dict())  # Assuming ast has a .to_dict() method
    cursor.execute('INSERT INTO rules (rule_string, ast) VALUES (?, ?)', (rule_string, ast_json))
    conn.commit()
    rule_id = cursor.lastrowid
    conn.close()
    return rule_id

def get_rule_by_id(rule_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rules WHERE id = ?', (rule_id,))
    rule = cursor.fetchone()
    conn.close()

    if rule:
        rule_string = rule[1]
        ast_json = rule[2]
        # Deserialize the AST from JSON back into a Python object
        ast_data = json.loads(ast_json)
        return {"rule_string": rule_string, "ast_data": ast_data}
    else:
        return None

def create_rules_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_string TEXT,
        ast TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Run this function once to create the table
create_rules_table()
