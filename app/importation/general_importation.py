import json
import urllib.request
from urllib.error import URLError

import codecs
from app import db
from app.models.antenna import Antenna
from app.models.gsm_signal import GsmSignal
from app.models.ranking import Ranking
from app.models.report import Report
from config import AppTokens
from config import ServerSettings
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

urls = ServerSettings.urls
SERVER_BASE_URL = urls["server_url"]
ANTENNA_URL = urls["antenna_url"]
REPORT_URL = urls["report_url"]
RANKING_URL = urls["ranking_url"]
NETWORK_URL = urls["network_url"]
SIGNAL_URL = urls["signal_url"]
reader = codecs.getreader("utf-8")
token = AppTokens.tokens["server"]
header = {"Authorization": "token " + token}


def report_import(year, month):
    url = SERVER_BASE_URL + "/" + REPORT_URL + "/" + str(year) + "/" + str(month)
    request = urllib.request.Request(url, headers={"Authorization": "token " + token})
    try:
        response = urllib.request.urlopen(request)
        data = json.load(reader(response))
        for type, element in data.items():
            try:
                for carrier, quantity in element.items():
                    carrier_id = int(carrier)
                    db.session.add(Report(year, month, type, carrier_id, quantity))
                    try:
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()
                        report = Report.query.filter_by(year=year, month=month, type=type,
                                                        carrier_id=carrier_id).first()
                        report.quantity = quantity
                        db.session.commit()
            except AttributeError:
                carrier_id = 0
                try:
                    db.session.add(Report(year, month, type, carrier_id, element))
                    db.session.commit()
                except:
                    db.session.rollback()
                    report = Report.query.filter_by(year=year, month=month, type=type,
                                                    carrier_id=carrier_id).first()
                    report.quantity = element
                    db.session.commit()

    except URLError:
        print("Can not access to ", url)

    except ValueError:
        print("Url is not valid")


def ranking_import(year, month):
    url = SERVER_BASE_URL + "/" + RANKING_URL + "/" + str(year) + "/" + str(month)
    request = urllib.request.Request(url, headers={"Authorization": "token " + token})
    try:
        response = urllib.request.urlopen(request)
        data = json.load(reader(response))
        for carrier, dict in data.iteritems():
            for traffic_type, dict in dict.items():
                for transfer_type, rank in dict.items():
                    carrier_id = int(carrier)
                    db.session.add(Ranking(year=year, month=month, carrier_id=carrier_id, traffic_type=traffic_type,
                                           transfer_type=transfer_type, rank=rank))
                    try:
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()
                        ranking = Ranking.query.filter_by(year=year, month=month, carrier_id=carrier_id,
                                                          traffic_type=traffic_type,
                                                          transfer_type=transfer_type).first()
                        ranking.rank = rank
                        db.session.commit()



    except URLError:
        print("Can not access to ", url)

    except ValueError:
        print("Url is not valid")


def gsm_signal_import(year, month):
    url = SERVER_BASE_URL + "/" + RANKING_URL + "/" + str(year) + "/" + str(month)
    request = urllib.request.Request(url, headers={"Authorization": "token " + token})
    try:
        response = urllib.request.urlopen(request)
        signals = json.load(reader(response))
        for signal in signals:
            antenna_id = signal["antenna_id"]
            carrier_id = signal["carrier_id"]
            quantity = signal["observations"]
            signal_mean = signal["signal_mean"]
            antenna = Antenna.query.get(signal["antenna_id"])
            if not antenna:
                get_antenna(antenna_id)
                antenna = Antenna.query.get(signal["antenna_id"])

            db.session.add(GsmSignal(year=year, month=month, antenna_id=antenna_id, carrier_id=carrier_id,
                                     signal=signal_mean, quatity=quantity))
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                signal = GsmSignal.query.filter_by(year=year, month=month, carrier_id=carrier_id,
                                                   antenna_id=antenna_id).first()
                signal.quantity = quantity
                signal.signal = signal_mean
                db.session.commit()

    except URLError:
        print("Can not access to ", url)

    except ValueError:
        print("Url is not valid")


def get_antenna(id):
    url = SERVER_BASE_URL + "/" + ANTENNA_URL + "/" + str(id)
    request = urllib.request.Request(url, headers={"Authorization": "token " + token})
    try:
        response = urllib.request.urlopen(request)
        data = json.load(reader(response))
        print(data)
        carrier_id = data["carrier_id"]
        cid = data["cid"]
        lac = data["lac"]
        lat = data["lat"]
        lon = data["lon"]
        db.session.add(Antenna(id=id, cid=cid, lac=lac, lat=lat, lon=lon, carrier_id=carrier_id))
        try:
            db.session.commit()
        except IntegrityError:
            try:
                db.session.rollback()
                antenna = Antenna.query.filter_by(id=id).first()
                antenna.lat = lat
                antenna.lon = lon
                db.session.commit()
            except:
                pass

    except ValueError:
        print("Url is not valid")


def antennas_import():
    id = db.session.query(func.max(Antenna.id))[0][0] + 1
    while (True):
        try:
            get_antenna(id)
        except URLError:
            break
        id = id + 1
