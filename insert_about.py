import sqlite3

# Connect to the database
conn = sqlite3.connect(r"C:\Users\Riti\Desktop\type2talk_web\db\database.db")
cursor = conn.cursor()

# Delete all existing "About" rows
cursor.execute("DELETE FROM menu WHERE name = ?", ('about',))

# Insert a fresh "About" menu item
cursor.execute("""
    INSERT INTO menu (name, text, icon, viewclass, parent_id)
    VALUES (?, ?, ?, ?, ?)
""", ('about', 'About', 'about', 'IconMenuItem', None))

# Commit changes
conn.commit()
print("Old About rows removed, new About row added successfully!")

# Optional: display all menu items to verify
cursor.execute("SELECT * FROM menu")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
