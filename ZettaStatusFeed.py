"""
    Zetta Status Feed Client
    v1.0.0
    Anthony Eden (http://mediarealm.com.au/)
"""

from pysimplesoap.client import SoapClient
import calendar
from datetime import datetime, timedelta

import ZettaCodes


# Stores the client connection
client = None


def connect(Address, Port = "3132", Debug = False):
    # Connect to the Status Feed API
    global client
    client = SoapClient(
        wsdl = "http://"+Address+":"+Port+"/StatusFeed?wsdl",
        trace=Debug
    )

def helper_UTCToLocal(datetime_utc):
    # From https://stackoverflow.com/a/13287083
    if datetime_utc is None:
        return None
    
    timestamp = calendar.timegm(datetime_utc.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert datetime_utc.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond = datetime_utc.microsecond)

def listStations():
    response = client.GetStations()

    if 'Station' in response['GetStationsResult']:
        return_data = []
        for station in response['GetStationsResult']['Station']:
                return_data.append({'Station': station})
        return return_data

    return response['GetStationsResult']

def stationMetadata(stationId):
    response = client.GetStationFull(stationId)
    data = response['GetStationFullResult']['Metadata']
    data['Name'] = response['GetStationFullResult']['Name']
    data['ID'] = response['GetStationFullResult']['ID']
    return data

def stationStatus(stationId):
    status = stationMetadata(stationId)['Status']
    return ZettaCodes.SequencerStatus(status)

def stationMode(stationId):
    mode = stationMetadata(stationId)['Mode']
    return ZettaCodes.SequencerMode(mode)

def stationTiming(stationId):
    return {
        "GapTimeInSeconds": stationMetadata(stationId)['GapTimeInSeconds'],
        "GapTimeTargetUtc": stationMetadata(stationId)['TargetGapTimeUtc'],
        "GapTimeTarget": helper_UTCToLocal(stationMetadata(stationId)['TargetGapTimeUtc']),
    }

def stationQueue(stationId):
    response = client.GetStationFull(stationId)
    queue = response['GetStationFullResult']['Queue']

    if 'Event' in queue:
        enumerate_data = []
        for x in queue['Event']:
            enumerate_data.append({'Event': x})
    else:
        enumerate_data = queue

    # Calculate local times and translate codes
    for i,item in enumerate(enumerate_data):
        enumerate_data[i]['Event']['AirTime'] = helper_UTCToLocal(item['Event']['AirTimeUtc'])
        enumerate_data[i]['Event']['AssetType'] = ZettaCodes.AssetType(item['Event']['AssetType'])
        enumerate_data[i]['Event']['ChainType'] = ZettaCodes.ChainType(item['Event']['ChainType'])
        enumerate_data[i]['Event']['EditCode'] = ZettaCodes.Edit(item['Event']['EditCode'])
        enumerate_data[i]['Event']['Status'] = ZettaCodes.EventStatus(item['Event']['Status'])

    return enumerate_data

def stationQueueNextStop(stationId):
    # Finds the time of the next stop for the given station
    queue = stationQueue(stationId)

    if stationStatus(stationId) != "ON-AIR":
        return None
    
    for item in queue:
        if item['Event']['ChainType'] == "Stop":
            return item['Event']['AirTime'] + timedelta(seconds = item['Event']['DurationToSegueInSeconds'])

    return None

