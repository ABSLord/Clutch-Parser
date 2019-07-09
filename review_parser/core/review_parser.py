import csv
import requests
from bs4 import BeautifulSoup


FIELDS = ["agency_town", "agency_county", "reviewer_name", "position",
          "company", "location", "project_summary", "feedback", "start_date",
          "finish_date", "budget"]


def review_parser(file_name):
    page = requests.get(
        "https://clutch.co/developers/python-django?field_pp_location_country_select=ru")
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        pages_num = int(soup.find_all('li', class_='pager-current')[0].contents[0].split(" of ")[1])
    except (IndexError, ValueError):
        pages_num = 0
    reviews_links = []
    for i in range(pages_num):
        if i > 0:
            page = requests.get(
                "https://clutch.co/developers/python-django?field_pp_location_country_select=ru&page={0}".format(i))
            soup = BeautifulSoup(page.content, 'html.parser')
        reviews_pages = soup.find_all('span', class_='reviews-count')
        reviews_links += [page.contents[0].attrs['href']
                          for page in reviews_pages]
    with open(file_name, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(FIELDS)
        for link in reviews_links:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            agency_location = soup.find_all("span", class_="location-name")[0].text.strip()
            agency_town, agency_county = agency_location.split(",")
            reviews = soup.find_all("div", class_="client-interview")
            for review in reviews:
                try:
                    project_summary = review.find_all("div", class_="field-name-field-fdb-proj-description")[0].text.split(":")[1].strip()
                except IndexError:
                    project_summary = ""

                try:
                    project_length = review.find_all("div", class_="field-name-field-fdb-project-length")[0].text
                    start_date, finish_date = project_length.strip().split("-")
                except(IndexError, ValueError):
                    start_date, finish_date = "", ""

                try:
                    budget = review.find_all("div", class_="field-name-field-fdb-cost")[0].text.strip()
                except IndexError:
                    budget = ""

                try:
                    feedback = review.find_all("div", class_="field-name-field-fdb-comments")[0].text.split(":")[1].strip()
                except IndexError:
                    feedback = ""

                try:
                    reviewer_name = review.find_all("div", class_="field-name-field-fdb-full-name-display")[0].text.strip()
                except IndexError:
                    reviewer_name = ""

                try:
                    position, company = review.find_all("div", class_="field-name-field-fdb-title")[0].text.strip().split(",")
                except(IndexError, ValueError):
                    position, company = "", ""

                try:
                    location = review.find_all("div", class_="field-name-field-fdb-location")[0].text.strip()
                except IndexError:
                    location = ""

                row = [agency_town, agency_county, reviewer_name, position,
                       company, location, project_summary, feedback,
                       start_date, finish_date, budget]
                csvwriter.writerow(row)


if __name__ == '__main__':
    review_parser("test.csv")
