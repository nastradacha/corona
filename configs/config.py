import json


def json_reader(file_path):
    """
    :param file_path: json file containing json file eg: login credentials or other input files
    :return: a dictionary object containing the username and password
    """
    with open(file_path) as json_file:
        json_file = json.load(json_file)
    return json_file


config = json_reader(
    "C:/Users/Nastracha/projects/corona/configs/config.json"
)  # read json file

# Page URL
ga_dept_health = config["URL"]["GA_dept_health"]


# Chrome browser
chrome_driver = config["Driver"]["Chrome_driver"]
# chrome_driver = chrome_driver

# Page Elements xpath
georgia_death_tab = config["Elements"]["georgia_death_tab"]
georgia_deaths_html = config["Elements"]["georgia_deaths_html"]
covid_status_grid_elem = config["Elements"]["covid_status_grid_elem"]
TotalTest_elem = config["Elements"]["TotalTest_elem"]
ConfirmedCases_elem = config["Elements"]["ConfirmedCases_elem"]
ICU_Admissions_elem = config["Elements"]["ICU_Admissions_elem"]
Hospitalized_elem = config["Elements"]["Hospitalized_elem"]
Deaths_elem = config["Elements"]["Deaths_elem"]
GA_status_url_link = config["Elements"]["GA_status_url_link"]


# File paths
covid_status_csv = config["file_paths"]["covid_status_csv"]
covid_status_html = config["file_paths"]["covid_status_html"]
covid_status_pdf = config["file_paths"]["covid_status_pdf"]
covid_death_detail_csv = config["file_paths"]["covid_death_detail_csv"]

