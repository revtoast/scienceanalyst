import sqlite3
import pandas as pd
# Create your connection.
cnx = sqlite3.connect('DB/parser.db')

df = pd.read_sql_query("SELECT * FROM twitter_icurehab", cnx)

print(df.head())
