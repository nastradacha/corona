import datetime
import matplotlib.pyplot as plt
import pandas as pd
from configs.config import *
from configs.config import ga_dept_health, georgia_death_tab, georgia_deaths_html
from main_modules.modules import browser
from PIL import Image
from io import BytesIO
import urllib
from time import sleep
from pathlib import Path
from selenium.webdriver import ActionChains
from whatsapp import send_to_phone

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pdf_file = "/tmp/demo.pdf"
# from pandas.plotting import table
csv_df = pd.read_csv(
    r"C:\Users\Nastracha\OneDrive\Desktop\corona_data\covid_status.csv"
)


today = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
browser.get(ga_dept_health)
iframe = browser.find_element_by_tag_name("iframe")
browser.switch_to.frame(iframe)
browser.implicitly_wait(3)


def get_deaths_in_georgia():
    deaths_in_georgia = browser.find_element_by_xpath(georgia_death_tab)
    deaths_in_georgia.click()
    browser.implicitly_wait(2)
    deaths_in_georgia_html = browser.find_element_by_xpath(
        georgia_deaths_html
    ).get_attribute("innerHTML")
    return pd.read_html(deaths_in_georgia_html)[0]


def get_covid_status():
    data = {}
    df = pd.DataFrame(
        columns=[
            "DateTime",
            "TotalTest",
            "ConfirmedCases",
            "ICU Admissions",
            "Hospitalized",
            "Deaths",
        ]
    )
    covid_status_grid = browser.find_elements_by_css_selector(covid_status_grid_elem)
    data["DateTime"] = today
    for i in range(len(covid_status_grid) - 1):
        data["TotalTest"] = (
            covid_status_grid[i].find_element_by_xpath(TotalTest_elem).text
        )
        data["ConfirmedCases"] = (
            covid_status_grid[i].find_element_by_xpath(ConfirmedCases_elem).text
        )
        data["ICU Admissions"] = (
            covid_status_grid[i].find_element_by_xpath(ICU_Admissions_elem).text
        )
        data["Hospitalized"] = (
            covid_status_grid[i].find_element_by_xpath(Hospitalized_elem).text
        )
        data["Deaths"] = covid_status_grid[i].find_element_by_xpath(Deaths_elem).text
        df = df.append(data, ignore_index=True)
    return df


def run():
    status_df = get_covid_status()
    df_appended_to_exicting_file = status_df.append(csv_df, ignore_index=True)
    df_appended_to_exicting_file.to_csv(
        r"C:\Users\Nastracha\OneDrive\Desktop\corona_data\covid_status.csv", index=False
    )
    df_appended_to_exicting_file.to_html("tester.html")
    # html = df_appended_to_exicting_file.to_html()

    # html = '/tester.html'

    get_deaths_in_georgia().to_csv(
        r"C:\Users\Nastracha\OneDrive\Desktop\corona_data\covid_deaths_details.csv",
        index=False,
    )
    # This does not change focus to the new window for the driver.
    browser.execute_script("window.open('');")
    # sleep(3)
    # Switch to the new window
    browser.switch_to.window(browser.window_handles[1])
    browser.get(r"C:\Users\Nastracha\projects\corona\tester.html")
    browser.implicitly_wait(5)
    img = Image.open(
        BytesIO(browser.find_element_by_tag_name("table").screenshot_as_png)
    )
    rgb = Image.new("RGB", img.size, (255, 255, 255))  # white backgroung
    rgb.paste(img, mask=img.split()[3])  # paste using alpha channel as mask
    rgb.save("filename.pdf", "PDF", quality=100)
    # get_deaths_in_georgia().plot(kind='bar')
    # plt.show()
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[2])
    browser.get("https://filebin.net/")
    browser.implicitly_wait(3)
    current_dir = str(Path(__file__).parent) + r"\filename.pdf"
    print(current_dir)
    file_uploader = browser.find_element_by_css_selector("#fileField")
    file_uploader.send_keys(current_dir)
    url_page = browser.find_element_by_css_selector(
        "#fileDrop > div.container-fluid > table > tbody:nth-child(2) > tr > td:nth-child(1) > a"
    ).get_attribute("href")
    print(url_page)

    send_to_phone(url_page)
    #
    #
    # sleep(10)


if __name__ == "__main__":
    run()
    # browser.close()
    browser.quit()
