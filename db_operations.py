import scrape_weather
import sqlite3
from BDContextManager import UseDatabase


class DBOperations:

    with UseDatabase('weather.sqlite') as cursor:
        create_table = """create table weather
                    (id integer primary key autoincrement not null,
                     w_date text not null,
                     location text not null,
                     max_temp real not null,
                     min_temp real not null,
                     avg_temp real not null);"""

        cursor.execute(create_table)

        insert_data = """INSERT INTO weather (w_date,location, max_temp, min_temp, avg_temp) VALUES (?,?,?,?,?)"""

        weather = scrape_weather.weather_data()
        for item in weather.items():
            cursor.execute(insert_data,(item[0],"Winnipeg,MB",item[1]["Max"], item[1]["Min"], item[1]["Mean"]))









































#     def connection_db(self):
#         conn = sqlite3.connect("")
#         cur = conn.cursor()
#         cur.execute("""create table weather
#                     (id integer primary key autoincrement not null,
#                      w_date text not null,
#                      location text not null,
#                      max_temp real not null,
#                      min_temp real not null,
#                      avg_temp real not null);""")
#         conn.commit()
#         return conn
#
#     def insert_db(self, con, weather_data):
#         insert_query = """INSERT INTO weather (w_date,location, max_temp, min_temp, avg_temp) VALUES (?,?,?,?,?)"""
#         try:
#             with con:
#                 for item in weather_data.items():
#                     conn.execute(insert_query,(item[0],"Winnipeg,MB",item[1]["Max"], item[1]["Min"], item[1]["Mean"]))
#         except sqlite3.IntegrityError:
#             print("Can't add the same data twice.")
#         con.close()
#
#     def data_output(self):
#         conn = sqlite3.connect("weather.sqlite")
#         conn.row_factory = sqlite3.Row
#         cur = conn.execute("SELECT * FROM weather")
#         wearher_tulpe = cur.fetchall()
#         for t in wearher_tulpe:
#             print(dict(t))
#         conn.close()
#         return wearher_tulpe
#
#
# db = DBOperations()
# conn = db.connection_db()
# db.insert_db(conn, scrape_weather.weather_data())
# db.data_output()





