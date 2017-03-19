import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pandas as pd
import sqlite3


# Create your connection.
cnx = sqlite3.connect('DB/parser.db')

df = pd.read_sql_query("SELECT * FROM twitter_stock", cnx)
dataseries = df['date'].value_counts()
dataseries.sort_index(axis='index')

dataseries.index = pd.to_datetime(dataseries.index)
dataseries.plot(x='index', y='values')
plt.show()
#plt.savefig('test.png')
