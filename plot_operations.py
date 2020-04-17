from BDContextManager import UseDatabase
import matplotlib.pyplot as plt
import datetime
import calendar
import pprint


class PlotOperations:
    def __init__(self, first_year=1996, last_year=2020):
        self.month_temp = []
        self.year_temp = dict()
        self.first_year = first_year
        self.last_year = last_year

    def create_temp_dict(self):
        with UseDatabase('weather.sqlite') as cursor:
            w_data = """SELECT strftime('%m', date(w_date)), avg_temp 
                        FROM weather 
                        WHERE (strftime('%m', date(w_date)) BETWEEN '01'  AND '12') 
                        AND (strftime('%Y', date(w_date)) BETWEEN ? AND ? )  
                        ORDER BY strftime('%m', date(w_date)); """

            cursor.execute(w_data, (str(self.first_year), str(self.last_year)))
            rows = cursor.fetchall()
            for x in range(1, 13):
                arr = []
                for row in rows:
                    if row[0].lstrip("0") == str(x) and type(row[1]) == float:
                        arr.append(row[1])
                self.year_temp.update({x: arr})
        return self.year_temp

    def populate_year_plot(self, dict_temp):
        fig, ax = plt.subplots()
        ax.boxplot(dict_temp.values())
        ax.set_xticklabels(dict_temp.keys())
        ax.set_title("Monthly Temperature Distribution for " + str(self.first_year) + " to " + str(self.last_year))
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')
        plt.show()

    def populate_single_month_plot(self, _month, _year):
        with UseDatabase('weather.sqlite') as cursor:
            monthly_data = """SELECT strftime('%m', date(w_date)), avg_temp 
                              FROM weather 
                              WHERE (strftime('%m', date(w_date)) = ? ) 
                              AND (strftime('%Y', date(w_date)) = ? )  
                              ORDER BY strftime('%m', date(w_date)); """
            cursor.execute(monthly_data, (str(_month).zfill(2), str(_year)))
            rows = cursor.fetchall()
            for row in rows:
                if type(row[1]) == float:
                    self.month_temp.append(row[1])

        plt.plot(self.month_temp)
        plt.ylabel('Temperature (Celsius)')
        plt.xlabel('Day')
        plt.title('Daily Temperature in ' + str(datetime.date(year=_year, month=_month, day=1).strftime('%B'))
                  + ' Distribution for : ' + str(_year))
        plt.show()


if __name__ == '__main__':
    p = PlotOperations(2000, 2017)
    year_temp = p.create_temp_dict()
    # pprint.pp(year_temp)
    p.populate_year_plot(year_temp)
    # p.populate_single_month_plot(4, 2016)
