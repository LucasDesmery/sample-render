import sqlite3

conn = sqlite3.connect('c:/Proyectos propios/SampleMaster/render/mibase.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(newAnswer)")
columns = cursor.fetchall()

print("Columns in newAnswer:")
for col in columns:
    print(col)

conn.close()
