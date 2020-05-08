import datetime

import pandas as pd
from main_modules.modules import browser

# from pandas.plotting import table


today = datetime.datetime.now()
browser.get("https://dph.georgia.gov/covid-19-daily-status-report")
iframe = browser.find_element_by_tag_name("iframe")
browser.switch_to.frame(iframe)
browser.implicitly_wait(3)


def get_deaths_in_georgia():
    deaths_in_georgia = browser.find_element_by_xpath('//*[@id="react-tabs-8"]')
    deaths_in_georgia.click()
    browser.implicitly_wait(2)
    deaths_in_georgia_html = browser.find_element_by_xpath(
        '//*[@id="TopContainer"]/div/div/div/div[4]'
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
    ace = browser.find_elements_by_css_selector("#KPI1")
    data["DateTime"] = today
    for i in range(len(ace) - 1):
        data["TotalTest"] = (
            ace[i].find_element_by_xpath('//*[@id="KPI1"]/div[1]/div/p').text
        )
        data["ConfirmedCases"] = (
            ace[i].find_element_by_xpath('//*[@id="KPI1"]/div[2]/p').text
        )
        data["ICU Admissions"] = (
            ace[i].find_element_by_xpath('//*[@id="KPI1"]/div[3]/p').text
        )
        data["Hospitalized"] = (
            ace[i].find_element_by_xpath('//*[@id="KPI1"]/div[4]/p').text
        )
        data["Deaths"] = ace[i].find_element_by_xpath('//*[@id="KPI1"]/div[5]/p').text
        df = df.append(data, ignore_index=True)
    return df


def run():
    get_covid_status().to_csv(
        r"C:\Users\Nastracha\OneDrive\Desktop\corona_data\covid_status.csv", index=False
    )
    get_deaths_in_georgia().to_csv(
        r"C:\Users\Nastracha\OneDrive\Desktop\corona_data\covid_deaths_details.csv",
        index=False,
    )


if __name__ == "__main__":
    run()
    browser.close()
