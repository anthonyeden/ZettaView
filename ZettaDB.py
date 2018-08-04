"""
A class of reusable Zetta DB queries and helper methods
Created by Anthony Eden (http://mediarealm.com.au/)
"""

import os
import pypyodbc

class ZettaDB():

    def __init__(self, SQLConnectionString = 'DSN=ZettaDb1;'):
        # Setup Zetta SQL DB Connection:
        dbConn = pypyodbc.connect(SQLConnectionString)
        self.cur = dbConn.cursor()
    
    def findAssetByExternalID(self, ExternalID):
        assetQuery = '''
        SELECT
            Asset.ThirdPartyID,
            Asset.Title,
            Resource.StorageFile,
            AutoGen_AssetReadonlyReferences.ArtistID_1,
            Resource.ResourceID,
            Asset.AssetID
            FROM
                Asset,
                Resource,
                AssetToResource,
                AutoGen_AssetReadonlyReferences
            WHERE
                Asset.AssetID = AssetToResource.AssetID
                AND AssetToResource.isPrimaryResource = 1
                AND AssetToResource.ResourceID = Resource.ResourceID
                AND Asset.AssetID = AutoGen_AssetReadonlyReferences.AssetID
                AND ThirdPartyID = ?
        '''
            
        self.cur.execute(assetQuery, [str(ExternalID)])
            
        assetList = []
            
        for d in self.cur:
            assetList.append({
                "AssetID": str(d[5]),
                "ExternalID": str(d[0]),
                "Filename": d[2],
                "Title": str(d[1]),
                "Artist": self.getArtistName(d[3]),
                "FileFolder": self.getStorageFolderFromFilename(d[4]),
                "FileExtension": self.getExtensionFromFilename(d[2]),
                "ResourceID": str(d[4])
            })
            
        return assetList

    def findAssetByEventId(self, eventId):
        # Given an Event ID, find the Asset ID
        
        assetQuery = '''SELECT
            StationSpecificData.AssetID
        FROM
            [ZettaDB].[dbo].[LogEvent],
            [ZettaDB].[dbo].[StationSpecificData]
        WHERE LogEventID = ?
        AND LogEvent.StationSpecificDataId = StationSpecificData.StationSpecificDataId'''

        self.cur.execute(assetQuery, [str(eventId)])
            
        assetList = []
            
        for d in self.cur:
            return str(d[0])
            
        return None
    
    def assetMarkers(self, AssetID):
        # Gets the asset markers from every station,
        # and returns them as one merged dict

        markerQuery = '''
                SELECT
                Asset.AssetID,
                TrimInDuration,
                TrimOutDuration,
                SeguePoint,
                EarlySeguePoint,
                Intro1Duration,
                Intro2Duration,
                Intro3Duration

          FROM
          [ZettaDB].[dbo].[AutoGen_StationSpecificDataReadonlyReferences],
          [ZettaDB].[dbo].[StationSpecificDataToStation],
          [ZettaDB].[dbo].[StationSpecificData],
          [ZettaDB].[dbo].[Asset]

          WHERE StationSpecificDataToStation.StationSpecificDataID = StationSpecificData.StationSpecificDataId
          AND StationSpecificData.AssetID = Asset.AssetID
          AND StationSpecificDataToStation.StationSpecificDataID = AutoGen_StationSpecificDataReadonlyReferences.StationSpecificDataID
          AND Asset.AssetID = ?
        '''
            
        self.cur.execute(markerQuery, [str(AssetID)])
        
        markPoints = {
            "TrimInDuration": None,
            "TrimOutDuration": None,
            "SeguePoint": None,
            "EarlySeguePoint": None,
            "Intro1Duration": None,
            "Intro2Duration": None,
            "Intro3Duration": None,
        }
            
        for d in self.cur:
            if d[1] is not None:
                markPoints['TrimInDuration'] = d[1]

            if d[2] is not None:
                markPoints['TrimOutDuration'] = d[2]

            if d[3] is not None:
                markPoints['SeguePoint'] = d[3]

            if d[4] is not None:
                markPoints['EarlySeguePoint'] = d[4]

            if d[5] is not None:
                markPoints['Intro1Duration'] = d[5]

            if d[6] is not None:
                markPoints['Intro2Duration'] = d[6]

            if d[7] is not None:
                markPoints['Intro3Duration'] = d[7]

        # Calculate the total intro time:
        if markPoints['Intro3Duration'] is not None:
            markPoints['IntroDuration'] = markPoints['Intro3Duration']
        elif markPoints['Intro2Duration'] is not None:
            markPoints['IntroDuration'] = markPoints['Intro2Duration']
        elif markPoints['Intro1Duration'] is not None:
            markPoints['IntroDuration'] = markPoints['Intro1Duration']
        else:
            markPoints['IntroDuration'] = 0
        
        return markPoints 


    def getArtistName(self, artistId):
        # Take the Artist ID and return the Artist's name

        try:
            artistId = int(artistId)
        except:
            return None

        artistNameQuery = '''
        SELECT Artist.Name
        FROM Artist
        WHERE ArtistID = ?'''
        
        self.cur.execute(artistNameQuery, [artistId])
        
        for d in self.cur:
            return d[0]
        
        return ""

    def getStorageFolderFromFilename(self, filename):
        # Zetta stores 1000 items in each folder (e.g. from 1000 to 1999)
        # This is based on the ResourceID
        
        folder = unicode(filename).split("~")[0][:-3]

        if folder == "":
            folder = 0

        return int(folder)

    def getExtensionFromFilename(self, fullname):
        # Returns the file's extension name

        filename, file_extension = os.path.splitext(fullname)
        return file_extension

    def getStorageFullPath(self, sharePath, filename):
        # Given the path and Filename, return the full path
        fullPath = sharePath + str(self.getStorageFolderFromFilename(filename)) + "\\" + filename
    
        if os.path.isfile(fullPath):
            return fullPath
        else:
            return None
        

