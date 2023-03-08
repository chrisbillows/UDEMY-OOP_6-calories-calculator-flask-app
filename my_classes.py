from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from requests import get
from selectorlib import Extractor

class MyForm(FlaskForm):
    name = StringField('Name')
    weight = StringField('Weight')
    height = StringField('Height')
    age = StringField('Age')
    country = StringField('Country')
    city = StringField('City')
    submit = SubmitField('Submit')


class Calorie:
    """Represent amount of calories calculated with
    BMR = 10*weight + 6.25*height - 5*age + 5 - 10*temperature"""

    def __init__(self, weight, height, age, temperature):
        self.weight = weight
        self.height = height
        self.age = age
        self.temperature = temperature

    def calculate(self):
        pass


class Temperature:
    """
    Represent a temperature value extracted from the timeanddate.com/weather webpage.
    """

    def __init__(self, country, city):
        self.country = country
        self.city = city

    def get_temp(self):
        my_headers = {
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        my_url = f'https://www.timeanddate.com/weather/{self.country}/{self.city}'
        my_extractor = Extractor.from_yaml_file('temperature.yaml')

        r = get(my_url, headers=my_headers)
        my_html = r.text
        temp_html = my_extractor.extract(my_html)
        stripped_temp = temp_html['temp'].replace('\xa0°C', '')
        return stripped_temp


class UserEstimate:
    """Represent amount of calories calculated with
    BMR = 10*weight + 6.25*height - 5*age + 5 - 10*temperature"""

    def __init__(self, weight, height, age, temperature):
        self.weight = weight
        self.height = height
        self.age = age
        self.temperature = temperature

    def test_method(self):
        return f'User height is {self.height} and user weight is {self.weight}'

    def calculate_estimate(self):
        return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5 - 10 * self.temperature