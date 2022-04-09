from time import sleep

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from zoneinfo import ZoneInfo

from tatsu.exceptions import FailedParse
from django.core.exceptions import ObjectDoesNotExist

from calendar_app.models import Event, Country
from calendar_app.utils import get_calendar_to_city


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
            sleep(1)
            new_country = country.replace(' ', '-').lower()
            try:
                calendar = get_calendar_to_city(new_country)
                print(f'Parsing...{country}...............', end='')
                for event in calendar.events:
                    event = Event.objects.create(
                        title=event.name,
                        start_time=event.begin.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                        end_time=event.end.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                        official_holiday=True,
                        country_id=Country.objects.get(country=country).pk
                    )
                    event.save()
                print('DONE')
            except FailedParse:
                bad_country = Country.objects.filter(country=country)
                try:
                    bad_country.delete()
                    print(f'{country} DELETED')
                except ObjectDoesNotExist:
                    print(f'{country} has not been deleted')
