from bs4 import BeautifulSoup
import requests
from ics import Calendar


def get_all_countries():
    countries_list = []
    page = "https://www.officeholidays.com/countries"
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'lxml')
    countries = soup.find_all('div', class_='four omega columns')[0].find_all('a')
    for country in countries:
        countries_list.append(country.contents[1].strip())
    return countries_list


def get_calendar_to_city(country):
    url = f"https://www.officeholidays.com/ics/{country}"
    calendar = Calendar(requests.get(url).text)
    return calendar


def create_user_event_after_change_country(user_id, country_id):
    pass
    # user_holidays = UserEvent.objects.filter(
    #     user_id=user_id,
    # )
    # if user_holidays.exists():
    #     user_holidays.delete()
    # event_queryset = Event.objects.filter(country_id=country_id)
    # for event in event_queryset:
    #     UserEvent.objects.create(
    #         user_id=user_id,
    #         event_id=event.pk,
    #     )
