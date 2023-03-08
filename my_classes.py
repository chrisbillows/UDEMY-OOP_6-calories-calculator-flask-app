from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from requests import get
from selectorlib import Extractor

class MyForm(FlaskForm):
    """Represent a form for accepting user inputs required for calculating users daily
     calorie usage"""

    name = StringField('Name')
    weight = StringField('Weight (in kg)')
    height = StringField('Height (in cm)')
    age = StringField('Age')
    country = StringField('Country')
    city = StringField('City')
    submit = SubmitField('Submit')


class User:
    """Represent a user for calculating daily calorie usage"""

    def __init__(self, weight, height, age, temperature):
        self.weight = weight
        self.height = height
        self.age = age
        self.temperature = temperature

    def calculate_estimate_instructor_formula(self):
        return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5 - 10 * self.temperature

    # TODO: implement a second, more scientifically respected method
    # Harris–Benedict equation
    # Add male or female ask
    # Remove temperature from calculation - perhaps add a weather related comment
    # Harris–Benedict equations revised by Mifflin and St Jeor in 1990:
    # Men	BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5
    # Women	BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161

class Location:
    """
    Represent a user location for extracting a temperature value from the
    timeanddate.com/weather webpage.
    """

    def __init__(self, country, city):
        self.country = country
        self.city = city

    # scrape temperature
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

        # uses a selectorlib method
        # TODO: consolidate to function to use one scraping library
        my_extractor = Extractor.from_yaml_file('temperature.yaml')

        # TODO: add some error handling
        # confusion with 'uk' or 'england'
        # on website, london is uk. milton keynes and bristol england/uk.
        # bristol works with uk
        # but milton keynes works with england (or did it)

        r = get(my_url, headers=my_headers)
        my_html = r.text
        temp_html = my_extractor.extract(my_html)
        stripped_temp = str(temp_html['temp']).replace('\xa0°C', '')
        return float(stripped_temp)
