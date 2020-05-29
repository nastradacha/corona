import json
from pathlib import Path


def json_reader(file_path):
    """
    :param file_path: json file containing json file eg: login credentials or other input files
    :return: a dictionary object containing the username and password
    """
    with open(file_path) as json_file:
        json_file = json.load(json_file)
    return json_file


# read json file
config = json_reader(Path.cwd() / "configs/config.json")


# Page URL
class PageUrls:
    ga_dept_health = config["URL"]["GA_dept_health"]
    File_bin = config["URL"]["File_bin"]


# Chrome browser
chrome_driver = Path.home() / (config["Driver"]["Chrome_driver"])


# Page Elements xpath
class Elements:
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
class FilePath:
    covid_status_csv = Path.home() / (config["file_paths"]["covid_status_csv"])
    covid_status_html = str(Path.home() / (config["file_paths"]["covid_status_html"]))
    covid_status_pdf = str(Path.home() / (config["file_paths"]["covid_status_pdf"]))
    covid_death_detail_csv = Path.home() / (
        config["file_paths"]["covid_death_detail_csv"]
    )
    materialize_css = Path.home() / (config["file_paths"]["materialize_css"])
