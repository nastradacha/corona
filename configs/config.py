import json
import os
import datetime
from dateutil import *
#
# # x = datetime.datetime.strptime("Apr 7, 2020", '%M-%d-%y').strftime('%m/%d/%y')
# year = datetime.date.today().year
# edit = 'Feb. 11 - Mar 12, 2020'
# edit = edit.split('-')[1]
# edit = parser.parse(edit)
# edit = edit.strftime('%m-%d-%y')
# # edit2 = edit.endswith(year)
# # print(edit2)
# dt = parser.parse('Apr 7, 2020')
# dt = dt.strftime('%m-%d-%y')
# # bt = parser.parse('Feb. 11 - Mar 12, 2020')  ## ('Feb. 11 - Mar 12, 2020')
# print(year)
#
# # print(x)
# print('this is dt', dt)
# print('this is edit', edit)
# # print('this is bt', bt)
# exit()


def json_reader(file_path):
    """
    :param file_path: json file containing json file eg: login credentials or other input files
    :return: a dictionary object containing the username and password
    """
    with open(file_path) as json_file:
        json_file = json.load(json_file)
    return json_file


config = json_reader("C:/Users/Nastracha/projects/corona/configs/config.json")  # read json file

# Page URL
ga_dept_health = config["URL"]["GA_dept_health"]


# Chrome browser
chrome_driver = config["Driver"]["Chrome_driver"]
# chrome_driver = chrome_driver

# Page Elements xpath
grid_1 = config["Elements"]["grid_1"]
grid_2 = config["Elements"]["grid_2"]