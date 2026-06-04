import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

c.execute("UPDATE core_stage SET name='Заготовка' WHERE name='загатовка'")

tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
if 'core_stagetemplate' in tables:
    c.execute("UPDATE core_stagetemplate SET name='Заготовка' WHERE name='загатовка'")

conn.commit()
conn.close()
print("Fixed typo in database.")
