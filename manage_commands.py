from app import db
from app.data import initial_data_antennas
from app.data import initial_data_carriers
from flask_script import Command
from sqlalchemy.exc import IntegrityError
import json

class Test(Command):
    def run(self):
        import unittest
        testmodules = [
            'tests',
        ]

        suite = unittest.TestSuite()

        for t in testmodules:
            try:
                # If the module defines a suite() function, call it to get the suite.
                mod = __import__(t, globals(), locals(), ['suite'])
                suitefn = getattr(mod, 'suite')
                suite.addTest(suitefn())
            except (ImportError, AttributeError):
                # else, just load all the test cases from the module.
                suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

        unittest.TextTestRunner(verbosity=2).run(suite)


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


class PopulateAntennas(Command):
    def run(self):
        from app.models.carrier import Carrier
        from app.models.antenna import Antenna

        jsonvar = json.loads(initial_data_antennas.initial_data_antennas)
        for k, v in jsonvar.items():
            if k == "antennas":
                for json_element in v:
                    antenna = Antenna()
                    try:
                        mnc = json_element['mnc']
                        mcc = json_element['mcc']
                        carrier = Carrier.query.filter(Carrier.mnc == mnc and Carrier.mcc == mcc).first()
                        antenna.carriers.append(carrier)
                    except KeyError:
                        continue
                    for k, v in json_element.items():
                        if hasattr(antenna, k):
                            setattr(antenna, k, v)
                    try:
                        db.session.add(antenna)
                        db.session.commit()
                    except (IntegrityError, Exception):
                        db.session.rollback()
                        continue


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

    # Agregar carriers
    jsonvar = json.loads(initial_data_carriers.initial_data_carriers)
    for k, v in jsonvar.items():
        if k == "carriers":
            save_models(v, Carrier)

def populate_regions():
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

def populate_cities():
    from app.models.city import City
    from app.data.communes import commune_codes, region_code_by_commune_code
    for key, value in commune_codes.items():
        city = City(key, value, region_code_by_commune_code(key))
        try:
            db.session.add(city)
            db.session.commit()
        except (IntegrityError, Exception):
            db.session.rollback()
            continue

class PopulateRegions(Command):
    def run(self):
        populate_regions()

class PopulateCities(Command):

    def run(self):
        populate_cities()



def delete_db():
    db.drop_all(bind=None)

class DeleteDb(Command):
    def run(self):
        delete_db()

def example_report():
    from app.models.report import Report
    db.session.add(Report(2016, 5, "total_device_carrier", 7301,3))
    db.session.add(Report(2016, 5, "total_device_carrier", 7302,2))
    db.session.add(Report(2016, 5, "total_device_carrier", 7303,1))
    db.session.add(Report(2016, 5, "total_device_carrier", 7307,2))
    db.session.add(Report(2016, 5, "total_device_carrier", 7308,1))
    db.session.add(Report(2016, 5, "total_device_carrier", 7309,1))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7301, 8555))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7302, 702))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7303, 884))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7307, 9455))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7308, 24))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7309, 68))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7301, 3))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7302, 2))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7303, 1))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7307, 2))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7308, 1))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7309, 1))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

class ExampleReport(Command):
    def run(self):
        example_report()

def example_ranking():
    from app.models.ranking import Ranking
    data = {"Facebook" : 23003,
            "Google" : 3123213,
            "Adkintun" : 232,
            "Tinder" : 344,
            "Spotify" : 0}
    rank = Ranking(2016,5,0,"wifi","upload", data)
    data2 = {"Facebook" : 233,
            "Google" : 33213,
            "Adkintun" : 236752,
            "Tinder" : 344,
            "Spotify" : 4324}
    rank2 = Ranking(2016,5,0,"wifi","download", data2)
    try:
        db.session.add(rank)
        db.session.add(rank2)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

class ExampleRanking(Command):
    def run(self):
        example_ranking()

