from app import app
from flask import render_template, jsonify, request, json


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/reports')
def reports():
    return render_template('total-reports.html')

@app.route('/getReport')
def getReports():
    from app.models.report import Report

    year = request.args.get('year')
    month = request.args.get('month')
    reports = Report.query.filter_by(year=year, month=month).all()
    total_device_carrier = {}
    total_devices = 0
    total_gsm_carrier = {}
    total_gsm = 0
    total_sims_carrier = {}
    total_sims = 0
    for report in reports:
        if report.type == "total_device_carrier":
            total_device_carrier[report.carrier.name] = report.quantity
            total_devices += report.quantity
        elif report.type == "total_gsm_carrier":
            total_gsm_carrier[report.carrier.name] = report.quantity
            total_gsm += report.quantity
        else:
            total_sims_carrier[report.carrier.name] = report.quantity
            total_sims += report.quantity
    data = {"total_device_carrier": total_device_carrier,
            "total_devices": total_devices,
            "total_gsm_carrier": total_gsm_carrier,
            "total_gsm": total_gsm,
            "total_sims_carrier": total_sims_carrier,
            "total_sims": total_sims}
    return json.dumps(data)

@app.route('/getCarriers')
def getCarriers():
    from app.models.carrier import Carrier
    carriers = Carrier.query.with_entities(Carrier.id,Carrier.name).all()
    data = {}
    for carrier in carriers:
        data[carrier.id] = carrier.name
    return json.dumps(data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
