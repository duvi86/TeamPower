import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'team_power.db'

# --- Database initialization ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        cost_center_project TEXT,
        cost_center_sow TEXT,
        sow_number TEXT,
        po TEXT,
        amount REAL,
        category TEXT,
        type TEXT
    )''')
    conn.commit()
    conn.close()

# --- CRUD Operations ---
def add_transaction(date, ccp, ccs, sow, po, amount, category, type_):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO transactions (date, cost_center_project, cost_center_sow, sow_number, po, amount, category, type)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (date, ccp, ccs, sow, po, amount, category, type_))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception(f"Database error: {e}")
    finally:
        conn.close()

def get_transactions():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM transactions')
        rows = c.fetchall()
        # Use correct column names matching the database fields
        columns = ['id', 'date', 'cost_center_project', 'cost_center_sow', 
                  'sow_number', 'po', 'amount', 'category', 'type']
        return [dict(zip(columns, row)) for row in rows]
    except sqlite3.Error as e:
        raise Exception(f"Database error: {e}")
    finally:
        conn.close()

# --- Utility for dashboard KPIs ---
def get_transactions_df():
    import pandas as pd
    try:
        data = get_transactions()
        if not data:
            return pd.DataFrame(columns=['Date','Cost Center Project','Cost Center SOW',
                                      'SOW Number','PO','Amount','Category','Type'])
        df = pd.DataFrame(data)
        # Rename columns to display format
        df = df.rename(columns={
            'date': 'Date',
            'cost_center_project': 'Cost Center Project',
            'cost_center_sow': 'Cost Center SOW',
            'sow_number': 'SOW Number',
            'po': 'PO',
            'amount': 'Amount',
            'category': 'Category',
            'type': 'Type'
        })
        # Drop the id column as it's not needed for display
        if 'id' in df.columns:
            df = df.drop('id', axis=1)
        return df
    except Exception as e:
        # Return empty DataFrame on error
        return pd.DataFrame(columns=['Date','Cost Center Project','Cost Center SOW',
                                   'SOW Number','PO','Amount','Category','Type'])

init_db()
