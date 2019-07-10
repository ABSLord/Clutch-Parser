import csv
import requests
from bs4 import BeautifulSoup
import geocoder
from django.core.files import File


FIELDS = ["agency_town", "agency_county", "reviewer_name", "position",
          "company", "reviewer_town", "reviewer_country", "project_summary", "feedback", "start_date",
          "finish_date", "budget"]

#  countries=("ru", "ua", "by")


def get_address_by_string(string):
    try:
        loc = geocoder.yandex(string).json
        reviewer_town, reviewer_country = loc.get("city", ""), loc.get("country", "")
    except:
        reviewer_town, reviewer_country = string, string
    return reviewer_town, reviewer_country


def parse_clutch_by_country(file_name, country="ru"):
    page = requests.get(
        "https://clutch.co/developers/python-django?field_pp_location_country_select={0}".format(country))
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        pages_num = int(soup.find_all('li', class_='pager-current')[0].contents[0].split(" of ")[1])
    except (IndexError, ValueError):
        pages_num = 0
    reviews_links = []
    for i in range(pages_num):
        if i > 0:
            page = requests.get(
                "https://clutch.co/developers/python-django?field_pp_location_country_select={0}&page={1}".format(country, i))
            soup = BeautifulSoup(page.content, 'html.parser')
        reviews_pages = soup.find_all('span', class_='reviews-count')
        reviews_links += [page.contents[0].attrs['href'].replace("#reviews",
                                                                 "")
                          for page in reviews_pages]
    with open(file_name, "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        for link in reviews_links:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')

            try:
                review_pages_num = len(soup.find_all('ul', class_='pagination')[0].find_all('li')) - 2
            except IndexError:
                review_pages_num = 0

            for i in range(review_pages_num + 1):
                if i > 0:
                    page = requests.get(
                        "{}?page=0,{}".format(
                            link, i))
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
                        reviewer_town, reviewer_country = "", ""
                    else:
                        reviewer_town, reviewer_country = get_address_by_string(
                            location)

                    row = [agency_town, agency_county, reviewer_name, position,
                           company, reviewer_town, reviewer_country, project_summary, feedback,
                           start_date, finish_date, budget]
                    csvwriter.writerow(row)


def review_parser(countries, review_id):
    from review_parser.models import Review
    review = Review.objects.get(pk=review_id)
    with open(review.file_name, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(FIELDS)
    for country in countries:
        parse_clutch_by_country(review.file_name, country)
        print(country)

    with open(review.file_name, "r") as f:
        review.file.save(review.file_name, File(f))


if __name__ == '__main__':
    review_parser("test.csv", ("ru", "ua", "by"))
