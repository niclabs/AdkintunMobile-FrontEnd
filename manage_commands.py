import json

from app import db
from app.data import initial_data_carriers
from flask_script import Command, Option
from sqlalchemy.exc import IntegrityError


def save_models(elements, model_class):
    for json_element in elements:
        model = model_class()
        for k, v in json_element.items():
            setattr(model, k, v)
        db.session.add(model)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


class Populate(Command):
    def run(self):
        populate()

def populate():
    from app.models.carrier import Carrier
    from config import AdminUser
    from app.models.user import User
    from werkzeug.security import generate_password_hash

    user = User()
    user.first_name = AdminUser.first_name
    user.last_name = AdminUser.last_name
    user.login = AdminUser.login
    user.email = AdminUser.email
    user.password = generate_password_hash(AdminUser.password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    # We aggregate carriers
    jsonvar = json.loads(initial_data_carriers.initial_data_carriers)
    for k, v in jsonvar.items():
        if k == "carriers":
            save_models(v, Carrier)
    # We aggregate regions
    populate_regions()
    # We aggregate cities
    populate_cities()


def populate_regions():
    import requests

    from app.models.region import Region
    from app.data.regions import region_codes
    for key, value in region_codes.items():
        reg = Region(key, value)
        try:
            db.session.add(reg)
            db.session.commit()
        except (IntegrityError, Exception):
            db.session.rollback()
            continue
    for region in Region.query.all():
        name = region.name.replace(' ', '%20')
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(name))
        jsonResponse = r.json()
        if jsonResponse['status'] == 'OK':
            loc = jsonResponse['results'][0]['geometry']['location']
            region.lat = loc['lat']
            region.lon = loc['lng']
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


def populate_cities():
    from app.models.city import City
    from app.data.communes import commune_codes, region_code_by_commune_code
    from app.data.communes_location import communes_locations
    for key, value in commune_codes.items():
        city = City(key, value, region_code_by_commune_code(key))
        try:
            db.session.add(city)
            db.session.commit()
        except (IntegrityError, Exception):
            db.session.rollback()
            continue
    # Charges the location of the cities
    for commune in communes_locations:
        try:
            city = City.query.get(commune["id"])
            city.lat = commune["lat"]
            city.lon = commune["lon"]
            db.session.commit()
        except:
            db.session.rollback()


class DeleteDb(Command):
    def run(self):
        db.drop_all(bind=None)


class MonthlyImport(Command):
    def run(self):
        from app.importation.monthly_importation import monthly_import
        monthly_import()


class CityAntennas(Command):
    def run(self):
        import json
        import time
        import urllib.request
        import codecs

        from app.models.antenna import Antenna
        from app.data.communes import get_commune_code_by_name
        from app import db

        reader = codecs.getreader("utf-8")
        antennas = Antenna.query.all()
        size = len(antennas)

        for i in range(size):
            if (not (i + 1) % 200):
                print("Updated ", i, " antennas")
            lat = str(antennas[i].lat)
            lon = str(antennas[i].lon)
            url = "http://localhost/nominatim/reverse?format=json&lat=" + lat + "&lon=" + lon + "&zoom=18&addressdetails=1"
            city = "unknown"
            region = "unknown"
            try:
                response = urllib.request.urlopen(url)
                data = json.load(reader(response))
                if ('error' not in data):
                    if ('city' in data["address"]):
                        city = data["address"]["city"]
                    elif ('town' in data["address"]):
                        city = data["address"]["town"]
                    elif ('village' in data["address"]):
                        city = data["address"]["village"]
                    else:
                        region = data["address"]["state"]
                        raise UnknownCityError()

                    region = data["address"]["state"]
            except:
                print("Searching ", i, " in googlemaps")
                url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lon + "&sensor=false"
                response = urllib.request.urlopen(url)
                data = json.load(reader(response))
                if data["status"] == "OK":
                    found = False
                    for element in data["results"][0]["address_components"]:
                        if element["types"] == ["locality", "political"]:
                            city = element["long_name"]
                            found = True
                        if element["types"] == ["administrative_area_level_3", "political"] and not found:
                            city = element["long_name"]
                        if element["types"] == ["administrative_area_level_1", "political"]:
                            region = element["long_name"]
                time.sleep(1)
            try:
                antennas[i].city_id = get_commune_code_by_name(city)
                db.session.commit()
            except:
                db.session.rollback()


class UnknownCityError(Exception):
    pass

# Command for creating sample antennas
class ExampleAntennas(Command):
    def run(self):
        from app.models.antenna import Antenna
        from app.models.city import City
        from app.models.carrier import Carrier
        import random

        n_antennas = 100
        cities = City.query.all()
        carriers = Carrier.query.all()

        for i in range(n_antennas):
            city = random.choice(cities)
            while city.lat is None and city.lon is None:
                city = random.choice(cities)
            carrier = random.choice(carriers)
            while carrier == 0:
                carrier = random.choice(carriers)
            db.session.add(Antenna(i, None, None, city.lat, city.lon, carrier.id, city.id))

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

# Import data, asking the user the year and the month (Just for testing)
class GeneralImport(Command):
    def get_options(self):
        return [
            Option('-y', '--year', dest='year', default=0),
            Option('-m', '--month', dest='month', default=0),
        ]

    def run(self, year, month):
        from app.importation.general_importation import report_import, gsm_signal_import, gsm_count_import, ranking_import
        # Reports
        print('Importando reportes del año {} mes {} ... '.format(year,month))
        report_import(year, month)
        # Ranking
        print('Importando ranking del año {} mes {} ... '.format(year,month))
        ranking_import(year, month)
        # Gsm signal
        print('Importando gsm signal del año {} mes {} ... '.format(year,month))
        gsm_signal_import(year, month)
        # Gsm count
        print('Importando gsm count del año {} mes {} ... '.format(year,month))
        gsm_count_import(year, month)