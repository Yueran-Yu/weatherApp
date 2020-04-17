from plot_operations import PlotOperations
from datetime import datetime
import os


class WeatherProcessor:
    @staticmethod
    def prompt_enter():
        print('Enter the start year (1996 - ' + str(datetime.now().year) + '): ')
        s_year = int(input())
        print(
            'Enter the end year (1996 - ' + str(datetime.now().year) + ', end year must bigger than the start year): ')
        e_year = int(input())

        if s_year > 2020 or s_year < 1996 or e_year < 1996 or e_year > 2020:
            print('Your enter is invalid, please enter the year in the range.')
        else:
            get_data = PlotOperations(s_year, e_year)
            year_agp = get_data.create_temp_dict()
            get_data.populate_year_plot(year_agp)
        
        

WeatherProcessor.prompt_enter()
os.system("pause")

    
