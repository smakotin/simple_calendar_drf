from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from calendar_app.models import Country


def get_all_countries(*args, **kwargs):
    countries_list = []
    page = "https://www.officeholidays.com/countries"
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'lxml')
    countries_columns = soup.find_all('div', class_='four omega columns')
    for column in countries_columns:
        countries = column.find_all('a')
        for country in countries:
            countries_list.append(country.contents[1].strip())
    return countries_list


class Command(BaseCommand):

    def handle(self, *args, **options):
        countries = get_all_countries()
        for country in countries:
            country_obj = Country(country=country)
            try:
                country_obj.save()
            except IntegrityError:
                continue


