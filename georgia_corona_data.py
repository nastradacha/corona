import datetime
from io import BytesIO
from time import sleep

import pandas as pd
from PIL import Image

from configs.config import Elements, FilePath, PageUrls
from main_modules.modules import browser, check_exists_by_xpath
from whatsapp import send_to_phone

# from pandas.plotting import table

pd.options.display.max_columns = None
pd.options.display.max_rows = None
# pdf_file = "/tmp/demo.pdf"

csv_df = pd.read_csv(FilePath.covid_status_csv)

today = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
browser.get(PageUrls.ga_dept_health)
iframe = browser.find_element_by_tag_name("iframe")
browser.switch_to.frame(iframe)
browser.implicitly_wait(3)


class GeorgiaCovid:
    def __init__(self):
        self.status_df = None
        self.df = None
        self.pdf_url = None
        self.df_appended_to_existing_file = None

    def get_deaths_in_georgia(self):
        deaths_in_georgia = browser.find_element_by_xpath(Elements.georgia_death_tab)
        deaths_in_georgia.click()
        browser.implicitly_wait(2)
        deaths_in_georgia_html = browser.find_element_by_xpath(
            Elements.georgia_deaths_html
        ).get_attribute("innerHTML")
        return pd.read_html(deaths_in_georgia_html)[0]

    def get_covid_status(self):
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
        covid_status_grid = browser.find_elements_by_xpath(
            Elements.covid_status_grid_elem
        )
        data["DateTime"] = today
        for elements in covid_status_grid:
            data["TotalTest"] = elements.find_element_by_xpath(
                Elements.TotalTest_elem
            ).text
            data["ConfirmedCases"] = elements.find_element_by_xpath(
                Elements.ConfirmedCases_elem
            ).text
            data["ICU Admissions"] = elements.find_element_by_xpath(
                Elements.ICU_Admissions_elem
            ).text
            data["Hospitalized"] = elements.find_element_by_xpath(
                Elements.Hospitalized_elem
            ).text
            data["Deaths"] = elements.find_element_by_xpath(Elements.Deaths_elem).text
            self.df = df.append(data, ignore_index=True)

    def save_covid_status_to_csv(self, covid_status_df, csv_status_path):
        self.status_df = covid_status_df
        print(self.status_df)
        self.df_appended_to_existing_file = self.status_df.append(
            csv_df, ignore_index=True
        )
        self.df_appended_to_existing_file.to_csv(csv_status_path, index=False)

    def covid_status_to_html(self, html_status_path):
        table = self.df_appended_to_existing_file.to_html()
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
                    table=self.status_df.to_html(
                        classes=["striped", "centered", "highlight"]
                    )
                )
            )

    def convert_html_to_pdf(self, pdf_status_path, html_status_path):
        browser.execute_script("window.open('');")
        sleep(3)
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

    def convert_pdf_to_url(self, pdf_status_path):
        browser.execute_script("window.open('');")
        browser.switch_to.window(browser.window_handles[2])
        browser.get(PageUrls.File_bin)
        browser.implicitly_wait(3)
        # current_dir = str(Path(__file__).parent) + pdf_status_path
        current_dir = pdf_status_path
        print(current_dir)
        file_uploader = browser.find_element_by_css_selector("#fileField")
        file_uploader.send_keys(current_dir)
        browser.implicitly_wait(5)
        if check_exists_by_xpath(Elements.GA_status_url_link) is False:
            browser.implicitly_wait(5)
        self.pdf_url = browser.find_element_by_css_selector(
            Elements.GA_status_url_link
        ).get_attribute("href")

    def run(self):
        self.get_covid_status()
        self.save_covid_status_to_csv(self.df, FilePath.covid_status_csv)
        self.get_deaths_in_georgia().to_csv(FilePath.covid_death_detail_csv, index=False)
        self.covid_status_to_html(FilePath.covid_status_html)
        self.convert_html_to_pdf(FilePath.covid_status_pdf, FilePath.covid_status_html)
        self.convert_pdf_to_url(FilePath.covid_status_pdf)
        url_to_pdf = self.pdf_url

        send_to_phone(url_to_pdf)
        browser.quit()


# if __name__ == "__main__":
#     src = GeorgiaCovid()
#     src.run()
