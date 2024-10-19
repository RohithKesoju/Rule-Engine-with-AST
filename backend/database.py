import sqlite3

def connect_db():
    conn = sqlite3.connect('rules.db')
    return conn

def save_rule(rule_string, ast):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rules (rule_string, ast) VALUES (?, ?)', (rule_string, str(ast)))
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
    return rule

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
