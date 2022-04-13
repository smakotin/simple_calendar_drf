from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

import requests
from zoneinfo import ZoneInfo
from tatsu.exceptions import FailedParse
from bs4 import BeautifulSoup
from tqdm import tqdm

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
            country_obj = Country(country=country)
            try:
                country_obj.save()
            except IntegrityError:
                continue
        for country in tqdm(countries):
            new_country = country.replace(' ', '-').lower()
            event_obj_lst = []
            try:
                calendar = get_calendar_to_city(new_country)
                for event in calendar.events:
                    event_obj = Event(
                        title=event.name,
                        start_time=event.begin.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                        end_time=event.end.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                        official_holiday=True,
                        country_id=Country.objects.get(country=country).pk
                    )
                    if event_obj not in event_obj_lst:
                        event_obj_lst.append(event_obj)
                try:
                    Event.objects.bulk_create(event_obj_lst, ignore_conflicts=True)
                except IntegrityError:
                    print(f'.......Error when saving the event {event.name}, maybe duplicate')
                    continue
            except FailedParse:
                bad_country = Country.objects.filter(country=country)
                try:
                    bad_country.delete()
                    print(f'{country} DELETED')
                except ObjectDoesNotExist:
                    print(f'{country} has not been deleted')
