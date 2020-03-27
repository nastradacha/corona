import json

import requests as re
from dateutil.parser import parse

from bs4 import BeautifulSoup

georgia_health = re.get("https://dph.georgia.gov/covid-19-daily-status-report")
georgia_health_html = georgia_health.text
corona_soup = BeautifulSoup(georgia_health_html, "lxml")

# print(corona_soup.prettify())


class CoCo:
    def __init__(self):
        self.headline = None
        self.headline_details = None
        self.date_published = None
        self.confirm_case, self.Testing_by_Lab, self.confirmed_cases_by_county = (
            [],
            [],
            [],
        )

    def header_details(self):
        global header
        scripts = corona_soup.find_all("script")
        print(len(scripts))
        for script in scripts:
            if "Article" in script.text:
                header = json.loads(str(script.text))
        article = header["@graph"][0]
        self.headline = article["headline"]
        self.headline_details = article["description"]
        self.date_published = parse(article["dateModified"])  # strftime('%m-%d-%y')
        print(self.headline)
        print(self.headline_details)
        print(self.date_published)

    def get_confirm_cases(self):
        soup2 = corona_soup.find_all("tbody")
        list_items = [i.text for i in soup2]
        [
            y.append(x.split("\n"))
            for x, y in zip(
                list_items,
                [
                    self.confirm_case,
                    self.Testing_by_Lab,
                    self.confirmed_cases_by_county,
                ],
            )
        ]
        self.confirm_case = self.confirm_case[0][: len(self.confirm_case[0]) - 1]
        self.Testing_by_Lab = self.Testing_by_Lab[0][: len(self.Testing_by_Lab[0]) - 1]
        self.confirmed_cases_by_county = self.confirmed_cases_by_county[0][
            : len(self.confirmed_cases_by_county[0]) - 1
        ]
        print(self.confirm_case)
        print(self.Testing_by_Lab)
        print(self.confirmed_cases_by_county)

    def run(self):
        self.header_details()
        self.get_confirm_cases()


if __name__ == "__main__":
    src = CoCo()
    src.run()
