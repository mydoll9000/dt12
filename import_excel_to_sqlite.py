import pandas as pd
import sqlite3

print("BAT DAU IMPORT...")

excel_file = "tt12.xlsx"

df = pd.read_excel(excel_file)

conn = sqlite3.connect("tt12_pro.db")

df.to_sql("dinh_muc", conn, if_exists="replace", index=False)

conn.close()

print("IMPORT THANH CONG")