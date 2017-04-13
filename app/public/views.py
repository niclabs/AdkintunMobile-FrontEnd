from app import app, crossdomain, db
from flask import render_template, request, json, abort

from app.models.carrier import Carrier
from app.models.antenna import Antenna
from app.models.ranking import Ranking
from sqlalchemy import distinct, text

cors_origin = app.config['CORS_DOMAIN']


@app.route('/getCarriersWithAntennas')
@crossdomain(origin=cors_origin)
def getCarriersWithAntennas():

    carriers = Carrier.query.with_entities(distinct(Carrier.id), Carrier.name, Antenna.carrier_id). \
        filter_by(id=Antenna.carrier_id).all()
    carriers_list = [{'id': c.carrier_id, 'name': c.name} for c in carriers]
    return json.dumps(carriers_list)


@app.route('/getCarriersWithRanking')
@crossdomain(origin=cors_origin)
def getCarriersWithRanking():

    carriers = Carrier.query.with_entities(distinct(Carrier.id), Carrier.name, Ranking.carrier_id). \
        filter_by(id=Ranking.carrier_id).all()
    carriers_list = [{'id': c.carrier_id, 'name': c.name} for c in carriers]
    return json.dumps(carriers_list)


# View that handles the reports and return them in Json format
@app.route('/getReport')
@crossdomain(origin=cors_origin)
def getReports():
    from app.models.report import Report

    year = request.args.get('year')
    month = request.args.get('month')
    reports = Report.query.filter_by(year=year, month=month).all()
    total_device_carrier = {}
    total_gsm_carrier = {}
    total_sims_carrier = {}
    total_devices = 0
    total_gsm = 0
    total_sims = 0

    for report in reports:

        if report.type == "total_device_carrier":
            total_device_carrier[report.carrier.name] = report.quantity
        elif report.type == "total_gsm_carrier":
            total_gsm_carrier[report.carrier.name] = report.quantity
        elif report.type == "total_sims_carrier":
            total_sims_carrier[report.carrier.name] = report.quantity
        elif report.type == "total_sims":
            total_sims = report.quantity
        elif report.type == "total_gsm":
            total_gsm = report.quantity
        elif report.type == "total_devices":
            total_devices = report.quantity

    data = {"total_device_carrier": total_device_carrier,
            "total_devices": total_devices,
            "total_gsm_carrier": total_gsm_carrier,
            "total_gsm": total_gsm,
            "total_sims_carrier": total_sims_carrier,
            "total_sims": total_sims}

    return json.dumps(data)


def convert_to_watt(signal):
    return 10**((signal - 30)/10)


def convert_to_dbm(signal):
    import math
    return 30 + 10 * math.log10(signal)


def getNetworkName(network_type):
    networks = ["OTHER", "RTT", "CDMA", "EDGE", "EHRPD", "EVDO_0",
                "EVDO_A", "EVDO_B", "GPRS", "HSDPA", "HSPA", "HSPAP", "HSUPA", "IDEN", "LTE", "UMTS", "UNKNOWN"];
    network_name = networks[network_type]
    if network_name in ["GPRS", "EDGE", "CDMA", "RTT", "IDEN"]:
        return "2G"
    elif network_name in ["UMTS", "EVDO_0", "EVDO_A", "HSDPA", "HSUPA", "HSPA", "EVDO_B", "EHRPD", "HSPAP"]:
        return "3G"
    elif network_name in ["LTE"]:
        return "4G"
    else:
        return "Otras"


@app.route('/getGsmSignal')
@crossdomain(origin=cors_origin)
def get_gsm_signal():
    year = request.args.get('year')
    month = request.args.get('month')
    # check parameters
    try:
        int(year)
        if 12 < int(month) or 1 > int(month):
            return abort(404)
    except Exception:
        return abort(404)
    sql = text("""SELECT carrier_name, p25, p50, p75
                    FROM gsm_signal_statistic_by_carrier
                    WHERE year=:year AND month=:month""")
    signal_report = {}
    result = db.engine.execute(sql, {'year': year, 'month': month})
    for row in result:
        name = row['carrier_name']
        min = row['p25']
        med = row['p50']
        max = row['p75']
        signal_report[name] = {
            'min': min,
            'mediana': med,
            'max': max}
    return json.dumps(signal_report)


@app.route('/getNetwork')
@crossdomain(origin=cors_origin)
def get_network():
    year = request.args.get('year')
    month = request.args.get('month')
    # check parameters
    try:
        int(year)
        if 12 < int(month) or 1 > int(month):
            return abort(404)
    except Exception:
        return abort(404)

    sql = text("""SELECT carrier_name, network_type, quantity
                    FROM gsm_count_by_carrier
                    WHERE year=:year AND month=:month""")
    count = {}
    result = db.engine.execute(sql, {'year': year, 'month': month})
    for row in result:
        name = row['carrier_name']
        network = row['network_type']
        quantity = row['quantity']
        if name not in count:
            count[name] = {
                '2G': 0,
                '3G': 0,
                '4G': 0,
                'Otras': 0}
        count[name][network] = quantity
    return json.dumps(count)


def convertToGB(bytes):
    return round(bytes / 1073741824, 2)


@app.route('/getRanking')
@crossdomain(origin=cors_origin)
def getAppRanking():
    from app.models.ranking import Ranking

    year = request.args.get('year')
    month = request.args.get('month')
    traffic_type = request.args.get('traffic_type')
    transfer_type = request.args.get('transfer_type')
    carrier_id = request.args.get('carrier_id')
    ranking = Ranking.query.filter_by(year=year,
                                      month=month,
                                      carrier_id= carrier_id,
                                      traffic_type=traffic_type,
                                      transfer_type=transfer_type)

    wrapper = [{'ranking_number':e.ranking_number,
                'app_name':e.app_name,
                'total_bytes':e.total_bytes,
                'bytes_per_user':convertToGB(e.bytes_per_user),
                'total_devices':e.total_devices} for e in ranking]

    wrapper = sorted(wrapper, key= lambda x: x['ranking_number'])

    data = {"xaxis": [e['app_name'] for e in wrapper],
            "yaxis": [e['bytes_per_user'] for e in wrapper]}

    return json.dumps(data)


@app.route('/getAntennas')
def getAntennas():
    from app.models.carrier import Carrier
    from app.models.antenna import Antenna

    carriers = Carrier.query.all()
    idToName = {}
    carrier_id = request.args.get('carrier')
    antennas = Antenna.query.filter(Antenna.city_id != None).all()
    data = list(map(modelToDict, antennas))
    for carrier in carriers:
        idToName[carrier.id] = carrier.name
    response = {"data": data, "idToName": idToName}
    return json.dumps(response)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page-not-found.html'), 404


def modelToDict(model):
    return model.dict


@app.route('/getGsmCount')
@crossdomain(origin=cors_origin)
def getGsmCount():
    #from app.map.mapManagement import build, change
    from app.models.antenna import Antenna
    from app.models.carrier import Carrier
    from app.models.gsm_count import GsmCount

    # newZoom = float(request.args.get('zoom'))
    # lastZoom = request.args.get('lastZoom')

    # lastCarrier = request.args.get('lastCarrier')
    # bounds = json.loads(request.args.get('mapBounds'))
    # if not lastZoom:
    #     return json.dumps(build(newZoom, newCarrier, bounds))
    # else:
    #     return json.dumps(change(int(lastZoom), newZoom, lastCarrier, int(newCarrier), bounds))

    carrier = request.args.get('carrier')

    if carrier == "0":
        antennas = Antenna.query.all()
        gsmCount = GsmCount.query.all()
    else:
        antennas = Antenna.query.filter_by(carrier_id = carrier)
        gsmCount = GsmCount.query.filter_by(carrier_id = carrier)

    carriersKnown = Carrier.query.all()
    carrierIds = [c.id for c in carriersKnown]
    antennasData = {}

    for antenna in antennas:
        if antenna.carrier_id in carrierIds:
            antennasData[antenna.id] = {'lat': antenna.lat,
                                        'lon': antenna.lon,
                                        'carrier': Carrier.query.filter_by(id=antenna.carrier_id).first().name,
                                        '2G': 0,
                                        '3G': 0,
                                        '4G': 0,
                                        'Otras': 0,
                                        'Total': 0}

    for gsm in gsmCount:
        if gsm.antenna_id in antennasData:
            antennaDict = antennasData[gsm.antenna_id]
            antennaDict[getNetworkName(gsm.network_type)] += gsm.quantity
            antennaDict['Total'] += gsm.quantity

    print('Cantidad de antenas:', len(antennasData.keys()))

    antennasInfo = {'antennasData': antennasData,
                    'totalAntennas': len(antennasData.keys())}

    return json.dumps(antennasInfo)


@app.route('/healthCheck', methods=['GET'])
def health_check():
    try:
        # to check database we will execute raw query
        db.session.execute('SELECT 1')
    except Exception as e:
        return 'Database unavailable', 503

    return 'OK'
