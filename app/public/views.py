from app import app
from flask import render_template, request, json


@app.route('/')
def index():
    return render_template('index.html', carriers=getCarriers())


@app.route('/charts')
def charts():
    return render_template('charts.html', carriers=getCarriers())


@app.route('/reports')
def reports():
    return render_template('total-reports.html')


@app.route('/getReport')
def getReports():
    from app.models.report import Report

    year = request.args.get('year')
    month = request.args.get('month')
    Report.query.filter_by(year=year, month=month).first_or_404()
    reports = Report.query.filter_by(year=year, month=month).all()
    total_device_carrier = {}
    total_gsm_carrier = {}
    total_sims_carrier = {}
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


@app.route('/getRanking')
def getAppRanking():
    import operator
    from app.models.ranking import Ranking

    year = request.args.get('year')
    month = request.args.get('month')
    traffic_type = request.args.get('traffic_type')
    transfer_type = request.args.get('transfer_type')
    carrier_id = request.args.get('carrier_id')
    ranking = Ranking.query.filter_by(year=year, month=month, carrier_id=carrier_id, traffic_type=traffic_type,
                                      transfer_type=transfer_type).first_or_404()
    list = sorted(ranking.rank.items(), key=operator.itemgetter(1))
    data = {"xaxis": [tuple[0] for tuple in list],
            "yaxis": [tuple[1] for tuple in list]}
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


def getCarriers():
    from app.models.carrier import Carrier
    carriers = Carrier.query.with_entities(Carrier.id, Carrier.name).all()
    return carriers


def modelToDict(model):
    return model.dict