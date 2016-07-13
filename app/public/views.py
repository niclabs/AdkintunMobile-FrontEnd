from app import app
from flask import render_template, json, jsonify


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graficos')
def graphs():
    return render_template('graficos.html')

@app.route('/reportes')
def reports():
    return render_template('reportes-totales.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
