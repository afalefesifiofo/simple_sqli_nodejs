import sqlite3

# Connessione al database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Esegui una query per visualizzare tutte le tabelle
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    print(table)

# Esegui una query su una tabella specifica
cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Chiudi la connessione
conn.close()
