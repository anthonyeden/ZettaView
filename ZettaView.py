""" ZettaView: A simple HTML Log/Sequencer viewer for RCS Zetta """

__product__             = "ZettaView"
__version__             = "1.0.0"
__author__              = "Anthony Eden"
__copyright__           = "Copyright 2018, Media Realm"
__url__                 = "https://mediarealm.com.au/"

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/libs")

from flask import Flask
from flask import render_template
from flask import jsonify

import ZettaStatusFeed

import datetime
import time
import json


base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)
template_folder = os.path.join(base_dir, 'templates')
static_folder = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder = template_folder, static_folder = static_folder)


class DateTimeEncoder(json.JSONEncoder):
    # From https://stackoverflow.com/a/27058505
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

@app.before_first_request
def connect_statusfeed():
    # Connect to the status feed
    ZettaStatusFeed.connect(CONFIG['ZettaServer'])

@app.before_first_request
def get_stations():
    app.stations = ZettaStatusFeed.listStations()
    for station, stationData in enumerate(app.stations):
        app.stations[station]['Data'] = {}
        app.stations[station]['DataLastUpdated'] = 0
        app.stations[station]['gapTimeLastValue'] = 0
        app.stations[station]['gapTimeCountdownTarget'] = None
        app.stations[station]['gapTimeCountdownTargetFormatted'] = None

@app.route('/')
def view_stations():
    # Get a list of stations and render a list as HTML
    stations = []
    for station in app.stations:
        stations.append({
            "Name": station['Station']['Name'],
            "ID": station['Station']['ID'],
        })

    return render_template('stations.html', stations=stations)

@app.route('/view/<station_id>/')
def view_station(station_id=None):
    # Having selected a station, render the log/sequencer viewer
    return render_template('station.html', station_id=station_id)

@app.route('/data/<station_id>/')
def data_station(station_id=None):
    # Generate and send the current data for this station

    station = None
    station_index = None

    for stationi, station_data in enumerate(app.stations):
        if str(station_data['Station']['ID']) == str(station_id):
            station = station_data
            station_index = stationi
            break

    if station is None:
        return app.response_class(
            response=json.dumps({"Error": "Station not found"}, cls=DateTimeEncoder),
            status=404,
            mimetype='application/json'
        )

    timingData = ZettaStatusFeed.stationTiming(station_id)

    nextStop = ZettaStatusFeed.stationQueueNextStop(station_id)
    if nextStop is not None:
        nextStop = nextStop.strftime("%Y-%m-%d %H:%M:%S")
    else:
        nextStop = None

    etm = timingData['GapTimeTarget']
    if etm is not None:
        etm = etm.strftime("%Y-%m-%d %H:%M:%S")
    else:
        etm = None

    if station['gapTimeLastValue'] != timingData['GapTimeInSeconds'] and timingData['GapTimeInSeconds'] is not None:
        print "Update gap time"
        app.stations[station_index]['gapTimeLastValue'] = timingData['GapTimeInSeconds']
        app.stations[station_index]['gapTimeCountdownTarget'] = datetime.datetime.now() - datetime.timedelta(seconds = timingData['GapTimeInSeconds'])
        app.stations[station_index]['gapTimeCountdownTargetFormatted'] = app.stations[station_index]['gapTimeCountdownTarget'].strftime("%Y-%m-%d %H:%M:%S")

    eventQueue = ZettaStatusFeed.stationQueue(station_id)
    currentEvent = eventQueue[0]['Event']
    currentEventId = currentEvent['EventID']
    
    data = {
        "station_id": station_id,
        "stationName": station['Station']['Name'],
        "status": ZettaStatusFeed.stationStatus(station_id),
        "mode": ZettaStatusFeed.stationMode(station_id),
        "nextStop": nextStop,
        "gapTime": timingData['GapTimeInSeconds'],
        "gapTimeCountdownTarget": station['gapTimeCountdownTargetFormatted'],
        "etm": etm,
        "eventQueue": eventQueue,
        }
    
    station['DataLastUpdated'] = time.time()
    station['Data'] = data
    
    return app.response_class(
        response=json.dumps(data, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    config_filename = os.path.join(application_path, "config.json")

    try:
        Config_JSON = open(config_filename).read()
        CONFIG = json.loads(Config_JSON)
    except Exception, e:
        print "ERROR LOADING CONFIG.JSON:", e
    else:
        app.run(host = '0.0.0.0', port = CONFIG['LocalPortNumber'])