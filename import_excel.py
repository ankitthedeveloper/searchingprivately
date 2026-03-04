import pandas as pd
import sqlite3

EXCEL_FILE = "records1.xlsx"

df = pd.read_excel(EXCEL_FILE)

# Rename columns if needed
df.columns = ["ID", "name", "father_name", "address", "mobile"]

conn = sqlite3.connect("database.db")
df.to_sql("records", conn, if_exists="replace", index=False)
conn.close()

print("Database Created Successfully!")