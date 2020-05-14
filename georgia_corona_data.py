import datetime
import pandas as pd
from configs.config import *
from configs.config import ga_dept_health, georgia_death_tab, georgia_deaths_html
from main_modules.modules import browser, check_exists_by_xpath
from PIL import Image
from io import BytesIO
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
    covid_status_grid = browser.find_elements_by_xpath(covid_status_grid_elem)
    data["DateTime"] = today
    for elements in covid_status_grid:
        data["TotalTest"] = elements.find_element_by_xpath(TotalTest_elem).text
        data["ConfirmedCases"] = elements.find_element_by_xpath(
            ConfirmedCases_elem
        ).text
        data["ICU Admissions"] = elements.find_element_by_xpath(
            ICU_Admissions_elem
        ).text
        data["Hospitalized"] = elements.find_element_by_xpath(Hospitalized_elem).text
        data["Deaths"] = elements.find_element_by_xpath(Deaths_elem).text
        df = df.append(data, ignore_index=True)
    return df


def save_covid_status_to_csv_and_html(
    covid_status_df, csv_status_path, html_status_path
):
    status_df = covid_status_df
    print(status_df)
    df_appended_to_exicting_file = status_df.append(csv_df, ignore_index=True)
    df_appended_to_exicting_file.to_csv(csv_status_path, index=False)
    table = df_appended_to_exicting_file.to_html()
    with open(html_status_path, "w") as f:
        css_sample = f"""
<html>
    <head>
        <title> Georgia COVID-19 Updated Data</title>
        <link rel="stylesheet" href='C://Users//Nastracha//OneDrive//Desktop//corona_data//css//materialize.min.css'>
    </head>
    {table}
</html>"""
        f.write(
            css_sample.format(
                table=df_appended_to_exicting_file.to_html(classes=["striped", "centered", "highlight"])
            )
        )


def convert_html_to_pdf(pdf_status_path, html_status_path):
    browser.execute_script("window.open('');")
    # sleep(3)
    # Switch to the new window
    browser.switch_to.window(browser.window_handles[1])
    browser.get(html_status_path)
    browser.implicitly_wait(5)
    img = Image.open(
        BytesIO(browser.find_element_by_tag_name("table").screenshot_as_png)
    )
    rgb = Image.new("RGB", img.size, (255, 255, 255))  # white backgroung
    rgb.paste(img, mask=img.split()[3])  # paste using alpha channel as mask
    rgb.save(pdf_status_path, "PDF", quality=100)
    # get_deaths_in_georgia().plot(kind='bar')
    # plt.show()


def convert_pdf_to_url(pdf_status_path):
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[2])
    browser.get("https://filebin.net/")
    browser.implicitly_wait(3)
    # current_dir = str(Path(__file__).parent) + pdf_status_path
    current_dir = pdf_status_path
    print(current_dir)
    file_uploader = browser.find_element_by_css_selector("#fileField")
    file_uploader.send_keys(current_dir)
    browser.implicitly_wait(5)
    asd = check_exists_by_xpath(GA_status_url_link)
    print(asd)
    return browser.find_element_by_css_selector(GA_status_url_link).get_attribute(
        "href"
    )


def run():
    save_covid_status_to_csv_and_html(
        get_covid_status(), covid_status_csv, covid_status_html
    )
    get_deaths_in_georgia().to_csv(
        covid_death_detail_csv, index=False,
    )

    convert_html_to_pdf(covid_status_pdf, covid_status_html)
    url_to_pdf = convert_pdf_to_url(covid_status_pdf)

    send_to_phone(url_to_pdf)


if __name__ == "__main__":
    run()
    # browser.close()
    browser.quit()
