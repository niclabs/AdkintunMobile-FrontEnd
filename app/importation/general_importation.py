from app.models.antenna import Antenna
from app.models.report import Report
from app.models.ranking import Ranking
from config import server_settings
from app import db
import urllib.request, json
from urllib.error import URLError
import codecs
from sqlalchemy.exc import IntegrityError

SERVER_BASE_URL = server_settings["server_url"]
ANTENNA_URL = server_settings["antenna_url"]
REPORT_URL = server_settings["report_url"]
RANKING_URL = server_settings["ranking_url"]
reader = codecs.getreader("utf-8")


def report_import(year,month):
    url = SERVER_BASE_URL + "/" + REPORT_URL + "/" + year + "/" + month
    try:
        response = urllib.request.urlopen(url)
        data = json.load(reader(response))
        for type, element in data.items():
            try:
                for carrier,quantity in element.items():
                    carrier_id = int(carrier)
                    db.session.add(Report(year,month,type,carrier_id,quantity))
                    try:
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()
                        report = Report.query.filter_by(year = year, month=month, type=type,carrier_id = carrier_id).first()
                        report.quantity = quantity
                        db.session.commit()
            except AttributeError:
                carrier_id = 0
                db.session.add(Report(year, month, type, carrier_id, element))

    except URLError:
        print("Can not access to ",url)

    except ValueError:
        print("Url is not valid")

def ranking_import(year,month):
    url = SERVER_BASE_URL + "/" + RANKING_URL + "/" + year + "/" + month
    try:
        response = urllib.request.urlopen(url)
        data = json.load(reader(response))
        for carrier, dict in data.iteritems():
            for traffic_type, dict in dict.items():
                for transfer_type, rank in dict.items():
                    carrier_id = int(carrier)
                    db.session.add(Ranking(year=year,month=month,carrier_id=carrier_id, traffic_type=traffic_type, transfer_type=transfer_type, rank=rank))
                    try:
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()
                        ranking = Ranking.query.filter_by(year = year, month = month, carrier_id=carrier_id, traffic_type=traffic_type, transfer_type=transfer_type)
                        ranking.rank = rank
                        db.session.commit()



    except URLError:
        print("Can not access to ", url)

    except ValueError:
        print("Url is not valid")


def get_antennas():
    url = SERVER_BASE_URL + "/" + ANTENNA_URL
    try:
        response = urllib.request.urlopen(url)
        data = json.load(reader(response))
        for row in data:
            carrier_id = int(str(row["mcc"])+str(row["mnc"]))
            cid = row["cid"]
            lac = row["lac"]
            lat = row["lat"]
            lon = row["lon"]
            db.session.add(Antenna(cid = cid,lac = lac,lat = lat,lon = lon, carrier_id = carrier_id))
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                antenna = Antenna.query.filter_by(cid=cid,lac=lac,carrier_id=carrier_id).first()
                antenna.lat = lat
                antenna.lon = lon
                db.session.commit()

    except URLError:
        print("Can not access to ", url)

    except ValueError:
        print("Url is not valid")
