from rest_framework.test import APITestCase
from calendar_app.models import Country


class CountryTests(APITestCase):

    def setUp(self):
        Country.objects.create(country='Angola')

    def test_country(self):
        country = Country.objects.get(country='Angola')
        print(country)
        self.assertEqual(country.pk, 1)


