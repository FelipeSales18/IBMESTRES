import sqlite3
import pandas as pd
import os

# File paths
excel_file = 'prototype/dataset/employees_scrum_db.xlsx'
db_file = 'prototype/dataset/employees.db'

# Ensure DB directory exists
db_dir = os.path.dirname(db_file)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Connect to SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create normalized tables
cursor.executescript('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    years_of_experience REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS competencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS employee_roles (
    employee_id INTEGER,
    role_id INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS employee_competencies (
    employee_id INTEGER,
    competency_id INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (competency_id) REFERENCES competencies(id)
);
''')

# Load Excel file
df = pd.read_excel(excel_file)

def get_or_create(cursor, table, value):
    cursor.execute(f'SELECT id FROM {table} WHERE name = ?', (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute(f'INSERT INTO {table} (name) VALUES (?)', (value,))
    return cursor.lastrowid

# Process each employee
for index, row in df.iterrows():
    name = row['Name']
    years = float(row['YearsExperience'])
    roles = [r.strip() for r in str(row['Roles']).split(',') if r.strip()]
    competencies = [c.strip() for c in str(row['Competencies']).split(',') if c.strip()]

    # Insert employee
    cursor.execute('INSERT INTO employees (name, years_of_experience) VALUES (?, ?)', (name, years))
    employee_id = cursor.lastrowid

    # Insert roles
    for role in roles:
        role_id = get_or_create(cursor, 'roles', role)
        cursor.execute('INSERT INTO employee_roles (employee_id, role_id) VALUES (?, ?)', (employee_id, role_id))

    # Insert competencies
    for comp in competencies:
        comp_id = get_or_create(cursor, 'competencies', comp)
        cursor.execute('INSERT INTO employee_competencies (employee_id, competency_id) VALUES (?, ?)', (employee_id, comp_id))

# Save and close
conn.commit()
conn.close()

print("Database populated successfully.")
