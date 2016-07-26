import json

from app import db
from app.data import initial_data_carriers
from flask_script import Command
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


class PopulateAntennas(Command):
    def run(self):
        from app.models.antenna import Antenna
        from app.data.communes import get_commune_code_by_name
        from app.data import data_antennas

        antennas = data_antennas.data_antennas
        for e in antennas:
            antenna = Antenna(e["cid"], e["lac"], e["lat"], e["lon"], int(str(e["mcc"]) + str(e["mnc"])),
                              get_commune_code_by_name(e["city"]))
            try:
                db.session.add(antenna)
                db.session.commit()
            except (IntegrityError, Exception):
                db.session.rollback()


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
    db.session.add(Report(2016, 5, "total_device_carrier", 7301, 3))
    db.session.add(Report(2016, 5, "total_device_carrier", 7302, 2))
    db.session.add(Report(2016, 5, "total_device_carrier", 7303, 1))
    db.session.add(Report(2016, 5, "total_device_carrier", 7307, 2))
    db.session.add(Report(2016, 5, "total_device_carrier", 7308, 1))
    db.session.add(Report(2016, 5, "total_device_carrier", 7309, 1))
    db.session.add(Report(2016, 5, "total_devices", 0, 10))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7301, 8555))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7302, 702))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7303, 884))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7307, 9455))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7308, 24))
    db.session.add(Report(2016, 5, "total_gsm_carrier", 7309, 68))
    db.session.add(Report(2016, 5, "total_gsm", 0, 19583))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7301, 3))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7302, 2))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7303, 1))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7307, 2))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7308, 1))
    db.session.add(Report(2016, 5, "total_sims_carrier", 7309, 1))
    db.session.add(Report(2016, 5, "total_sims", 0, 10))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


class ExampleReport(Command):
    def run(self):
        example_report()


def example_ranking():
    from app.models.ranking import Ranking
    data = {"Facebook": 23003,
            "Google": 3123213,
            "Adkintun": 232,
            "Tinder": 344,
            "Spotify": 0}
    rank = Ranking(2016, 5, 0, "wifi", "upload", data)
    data2 = {"Facebook": 233,
             "Google": 33213,
             "Adkintun": 236752,
             "Tinder": 344,
             "Spotify": 4324}
    rank2 = Ranking(2016, 5, 0, "wifi", "download", data2)
    try:
        db.session.add(rank)
        db.session.add(rank2)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


class ExampleRanking(Command):
    def run(self):
        example_ranking()


class MonthlyImport(Command):
    def run(self):
        from app.importation.monthly_importation import monthly_import
        monthly_import()
