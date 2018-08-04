"""
Zetta Code Mappings
Taken from the v4.1 Manual (Appendix / Zetta Codes)
"""

def AssetType(assettype):
    if assettype == 0:
        return "Invalid"
    elif assettype == 1:
        return "Song"
    elif assettype == 2:
        return "Spot"
    elif assettype == 3:
        return "Link"
    elif assettype == 4:
        return "VoiceTrack"

    return "Unknown-" + str(assettype)

def ChainType(chaintype):
    if chaintype == 0:
        return "Invalid"
    elif chaintype == 1:
        return "Segue"
    elif chaintype == 2:
        return "Auto Post"
    elif chaintype == 3:
        return "Stop"
    elif chaintype == 4:
        return "Link Song"

    return "Unknown-" + str(chaintype)

def Edit(code):
    if code == 0:
        return "Invalid"
    elif code == 100:
        return "Scheduler - Import"
    elif code == 101:
        return "Scheduler - Move"
    elif code == 102:
        return "Scheduler - Skipped"
    elif code == 103:
        return "Scheduler - Insert"
    elif code == 200:
        return "User - Insert"
    elif code == 201:
        return "User - Move"
    elif code == 202:
        return "User - Skipped"
    elif code == 203:
        return "User - Ejected"
    elif code == 204:
        return "User - Copy"
    elif code == 205:
        return "User - Synch to Selection Past"
    elif code == 206:
        return "User - Synch to Selection Future"
    elif code == 207:
        return "External App Modify"
    elif code == 208:
        return "External App Insert"
    elif code == 209:
        return "User Resolved"
    elif code == 220:
        return "Mini-Log - Insert By User"
    elif code == 221:
        return "Mini-Log - Skipped"
    elif code == 222:
        return "Mini-Log - Deleted"
    elif code == 223:
        return "Mini-Log - Insert By Clock"
    elif code == 300:
        return "Sequencer - Insert - Fill"
    elif code == 301:
        return "Sequencer - Move"
    elif code == 302:
        return "Sequencer - Resync"
    elif code == 303:
        return "Sequencer - Expired"
    elif code == 304:
        return "Sequencer - Insert - GPIO"
    elif code == 305:
        return "Sequencer - Live Event - Invalid Mode"
    elif code == 306:
        return "Sequencer - Insert - Master Fill"
    elif code == 401:
        return "Flat File Load - Insert"
    elif code == 402:
        return "Flat File Merge"
    elif code == 501:
        return "Splits - Insert"
    elif code == 502:
        return "Splits - Cued By Asset"
    elif code == 503:
        return "Splits - Cued By Tag"
    elif code == 504:
        return "Splits - Cued By Position"
    elif code == 505:
        return "Splits - Cued By ThirdParty"
    elif code == 506:
        return "Splits - Skipped"
    elif code == 507:
        return "Splits - Played on Client"
    elif code == 508:
        return "Splits - Cued By ETM"

    raise ValueError("Unknown Edit Code: " + str(code))

def EventStatus(code):
    if code == -3:
        return "Pending Played"
    elif code == 0:
        return "Invalid"
    elif code == 1:
        return "Ready"
    elif code == 2:
        return "Current"
    elif code == 3:
        return "Played"
    elif code == 4:
        return "Not Played"
    elif code == 5:
        return "Event_Error"
    elif code == 6:
        return "Faded Early"
    elif code == 7:
        return "Fade"
    elif code == 8:
        return "Stopped"
    elif code == 9:
        return "Paused"
    elif code == 10:
        return "Waiting Current"

    raise ValueError("Unknown Event Status Code: " + str(code))

def SequencerMode(mode):
    if mode == 1:
        return "AUTO"
    elif mode == 2:
        return "MANUAL"
    elif mode == 3:
        return "LIVE-ASSIST"
    elif mode == 4:
        return "SPLIT"
    elif mode == 5:
        return "SATELLITE"
    
    raise ValueError("Unknown Sequencer Mode: " + str(mode))

def SequencerStatus(status):
    if status == 0:
        return "UNKNOWN"
    elif status == 1:
        return "OFFLINE"
    elif status == 2:
        return "ON-AIR"
    elif status == 3:
        return "IDLE"
    elif status == 4:
        return "PLAYER_OFFLINE"
    elif status == 5:
        return "IDLE-PAUSED"
    elif status == 6:
        return "ON-AIR-PAUSED"
    elif status == 7:
        return "CONTENT_STORE_OFFLINE"

    raise ValueError("Unknown Sequencer Status: " + str(status))
