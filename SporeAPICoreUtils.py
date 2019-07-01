# -*- coding: utf-8 -*-
import urllib.request, urllib.error, urllib.parse
import xml.dom.minidom
import os
from datetime import datetime
from string import punctuation
import time

# Core Utils
# This is the core library that handles URL opening, XML parsing and basic data handling for all Spore API REST feeds
# You should create a "Downloads" directory wherever this file is kept since certain functions let you download assets
# See SporeAPIExamples.py for examples that use the functions in this file
# Email: sshodhan@maxis.com with questions


# Globals
serverString = "http://www.spore.com"
currentSaveDir = "./Downloads/"

statList = ["input", "cost", "height", "health", "meanness", "cuteness", "sense", \
            "bonecount", "footcount", "graspercount", "basegear", "carnivore", \
            "herbivore", "glide", "sprint", "stealth", "bite", "charge", \
            "strike", "spit", "sing", "dance", "gesture", "posture"]

statCompareList = ["cost", "height", "health", "meanness", "cuteness", "sense", \
                   "bonecount", "footcount", "graspercount", "basegear", "carnivore", \
                   "herbivore", "glide", "sprint", "stealth", "bite", "charge", \
                   "strike", "spit", "sing", "dance", "gesture", "posture"]


############# CONSTRUCT SPOREAPI URLS ##############

# Static Data URLS
def LargeCard(assetId):
    return "http://www.spore.com/sporepedia#qry=sast-" + assetId


def XMLURL(assetId):
    sub1 = assetId[0:3]
    sub2 = assetId[3:6]
    sub3 = assetId[6:9]
    return serverString + "/static/model/" + sub1 + "/" + sub2 + "/" + sub3 + "/" + assetId + ".xml"


def LargeAssetURL(assetId):
    sub1 = assetId[0:3]
    sub2 = assetId[3:6]
    sub3 = assetId[6:9]
    return serverString + "/static/image/" + sub1 + "/" + sub2 + "/" + sub3 + "/" + assetId + "_lrg.png"


def AssetURL(assetId):
    sub1 = assetId[0:3]
    sub2 = assetId[3:6]
    sub3 = assetId[6:9]
    return serverString + "/static/thumb/" + sub1 + "/" + sub2 + "/" + sub3 + "/" + assetId + ".png"


def BlockMapURL(blocktype):
    return serverString + "/www_static/data/Blocks/" + blocktype + ".xml"  # todo: change to lowercase


def PaintMapURL(blocktype):
    return serverString + "/www_static/data/Paints/" + blocktype + ".xml"  # todo: change to lowercase


# Things for a User URLS
def AssetsForUserURL(username, start, length):
    return serverString + "/rest/assets/user/" + username + "/" + str(start) + "/" + str(length)


def BuddiesForUserURL(username, start, length):
    return serverString + "/rest/users/buddies/" + username + "/" + str(start) + "/" + str(length)


def SporeCastsSubscribedURL(username):
    return serverString + "/rest/sporecasts/" + username


def AchievementsForUserURL(username, start, length):
    return serverString + "/rest/achievements/" + username + "/" + str(start) + "/" + str(length)


def ProfileForUserURL(username):
    return serverString + "/rest/user/" + username


# Things for an Asset URLS
def CommentsForAssetURL(assetId, start, length):
    return serverString + "/rest/comments/" + assetId + "/" + str(start) + "/" + str(length)


def StatsForCreatureURL(assetId):
    return serverString + "/rest/creature/" + assetId


def InfoForAssetURL(assetId):
    return serverString + "/rest/asset/" + assetId


# Assets for Sporecast
def AssetsForSporeCastURL(sporecastId, start, length):
    return serverString + "/rest/assets/sporecast/" + sporecastId + "/" + str(start) + "/" + str(length)


# Searches
def AssetSearch(searchType, start, length, assetType=""):
    return serverString + "/rest/assets/search/" + searchType + "/" + str(start) + "/" + str(length) + "/" + assetType


############# URL LOADING and XML PARSING ##############
def TryOpenURL(url):
    print("Getting " + url)
    try:
        f = urllib.request.urlopen(url)
        return f
    except:
        print(("ERROR OPENING: " + url))
        return ""


def UnicodeString(inputStr):
    return str(inputStr, 'latin-1').encode('utf-8')


def TryParseXML(xmlString):
    try:
        myxml = xml.dom.minidom.parseString(UnicodeString(xmlString))
        return myxml
    except:
        print("ERROR parsing XML")
        # raise
        return ""


def TryGetNodes(xml, nodename):
    try:
        return xml.getElementsByTagName(nodename)
    except:
        print(("ERROR XML Node: " + nodename))
        return ""


def TryGetNodeValues(xml, nodename):
    nodes = []
    try:
        elems = xml.getElementsByTagName(nodename)
    except:
        print(("ERROR XML NODE: " + nodename))
        return nodes

    for i in range(0, len(elems)):
        nodes.append(elems[i].firstChild.nodeValue)
    return nodes


def GetXMLForREST(url):
    f = TryOpenURL(url)
    if (f):
        myxml = TryParseXML(f.read())
        return myxml
    else:
        return ""


def GetTagValue(xml, tagName):
    if (xml.hasChildNodes):
        xmltag = xml.getElementsByTagName(tagName)
        if (xmltag.length > 0):
            return xmltag[0].firstChild.nodeValue
        else:
            print("GetTagValue: Couldn't find tag " + tagName)
            print(xmltag)
            print(xml.toxml())
    else:
        print("No children in xml passed to GetTagValue")
        print(tagName)
        print(xml.toxml())


############# FETCHING STUFF ##############

def FetchAndSave(url, filename):
    f = TryOpenURL(url)
    if (f):
        outfile = currentSaveDir + filename
        print("Saving " + outfile)
        fout = open(outfile, 'wb')
        fout.write(f.read())
        fout.close()


def FetchAndSaveSmallPNG(assetId):
    url = AssetURL(assetId)
    FetchAndSave(url, assetId + ".png")


def FetchAndSaveLargePNG(assetId):
    url = LargeAssetURL(assetId)
    FetchAndSave(url, assetId + "_lrg.png")


def FetchAndSaveXML(assetId):
    url = XMLURL(assetId)
    FetchAndSave(url, assetId + ".xml")


def FetchAndSaveBlockMap(mapName=""):
    url = BlockMapURL(mapName)
    FetchAndSave(url, mapName + ".xml")


def FetchAndSavePaintMap(mapName):
    url = PaintMapURL(mapName)
    FetchAndSave(url, mapName + ".xml")


############# CREATURE STATS ##############
class Stat:
    def __init__(self, xmlNode):
        self.mStats = {"": ""}
        for i in range(0, len(statList)):
            self.mStats[statList[i]] = GetTagValue(xmlNode, statList[i])

    def WriteToFile(self, f):
        keys = list(self.mStats.keys())
        for i in range(0, len(keys)):
            f.write(keys[i] + " " + str(self.mStats[keys[i]]) + "\n")

    def Print(self):
        keys = list(self.mStats.keys())
        for i in range(0, len(keys)):
            print(keys[i] + " " + str(self.mStats[keys[i]]))


def GetStatsForCreature(creatureId):
    url = StatsForCreatureURL(creatureId)
    myxml = GetXMLForREST(url)
    if (myxml):
        return Stat(myxml)
    return ""


############# SEARCHES ##############
def GetIdsSearch(searchType, start=0, length=100, assetType=""):
    url = AssetSearch(searchType, start, length, assetType)
    myxml = GetXMLForREST(url)
    ids = []
    if (myxml):
        ids = TryGetNodeValues(myxml, "id")  # you can extend this to get other nodes
    return ids


def FetchAssetsInSearch(searchType, start=0, length=100, assetType=""):
    ids = GetIdsSearch(searchType, start, length, assetType)
    for i in range(0, len(ids)):
        FetchAndSaveSmallPNG(ids[i])


############# COMMENTS ##############
class Comment:
    def __init__(self, message, sender, date):
        self.mMessage = message
        self.mSender = sender
        self.mDate = date


def MakeDateObject(dateStr):
    dateStr = dateStr.strip().split(" ")
    ymd = dateStr[0].strip().split("-")
    hms = dateStr[1].strip().split(":")
    s = hms[2].strip().split(".")
    newDate = datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), int(hms[0]), int(hms[1]), int(s[0]), int(s[1]))
    return newDate


def GetCommentsForAsset(assetid):
    url = CommentsForAssetURL(assetid, 0, 5000)
    myxml = GetXMLForREST(url)
    comments = []
    if (myxml):
        messages = TryGetNodeValues(myxml, "message")
        senders = TryGetNodeValues(myxml, "sender")
        dates = TryGetNodeValues(myxml, "date")
        for i in range(0, len(messages)):
            newDate = MakeDateObject(dates[i])
            # newDate = datetime.strptime(dateStr, "%y-%m-%d %H:%M:%S")
            # print newDate
            newComment = Comment(messages[i], senders[i], newDate)
            comments.append(newComment)
    return comments


############# ASSET INFO (Tags, Description) ##############
def GetDescriptionForAsset(assetid):
    url = InfoForAssetURL(assetid)
    myxml = GetXMLForREST(url)
    description = ""
    if (myxml):
        description = TryGetNodeValues(myxml, "description")
        if (description == "NULL" or description == "null"):
            description = ""
        myxml.unlink()
    return description


def GetTagsForAsset(assetid):
    url = InfoForAssetURL(assetid)
    myxml = GetXMLForREST(url)
    tags = []
    if (myxml):
        tagList = TryGetNodeValues(myxml, "tags")
        for i in range(0, len(tagList)):
            separatedTags = tagList[i].strip().split(",")
            for j in range(0, len(separatedTags)):
                if (separatedTags[j] != "NULL"):
                    tags.append(separatedTags[j].strip())
        myxml.unlink()
    return tags


############# User (assets, buddies, profile pic, sporecasts, achievements for user) ##############
def GetAssetIdsForUser(username, assettype=""):
    url = AssetsForUserURL(username, 0, 5000)
    myxml = GetXMLForREST(url)
    assetIds = ""
    if (myxml):
        assetIds = TryGetNodeValues(myxml, "id")
        myxml.unlink()
    return assetIds


def GetAssetIdsOfTypeForUser(username, assettype):
    url = AssetsForUserURL(username, 0, 5000)
    myxml = GetXMLForREST(url)
    assetIds = []
    if (myxml):
        assetIdList = TryGetNodeValues(myxml, "id")  # you can extend this to get other nodes
        modelTypeList = TryGetNodeValues(myxml, "type")
        for i in range(0, len(assetIdList)):
            if (modelTypeList[i] == assettype):
                assetIds.append(assetIdList[i])
        myxml.unlink()
    return assetIds


def GetAssetsForUser(username):
    url = AssetsForUserURL(username, 0, 5000)
    myxml = GetXMLForREST(url)
    if (myxml):
        assetids = TryGetNodes(myxml, "id")
        for i in range(0, len(assetids)):
            FetchAndSaveSmallPNG(assetids[i].firstChild.nodeValue)
        myxml.unlink()


def GetBuddiesForUser(username):
    url = BuddiesForUserURL(username, 0, 5000)
    myxml = GetXMLForREST(url)
    buddyList = []
    if (myxml):
        buddyNodes = TryGetNodes(myxml, "name")  # you can extend this to get other nodes
        for i in range(0, len(buddyNodes)):
            buddyList.append(buddyNodes[i].firstChild.nodeValue)
        myxml.unlink()
    return buddyList


def GetSporeCastsForUser(username):
    url = SporeCastsSubscribedURL(username)
    myxml = GetXMLForREST(url)
    casts = []
    if (myxml):
        casts = TryGetNodeValues(myxml, "id")  # you can extend this to get other nodes
        myxml.unlink()
    return casts


class Achievement:
    def __init__(self, aId, name, text):
        self.mId = aId
        self.mName = name
        self.mText = text


gAchievements = {"": Achievement("", "", "")}
gAchievementsGenerated = 0


def GenerateAchievementsList():
    url = "http://www.spore.com/data/achievements.xml"
    myxml = GetXMLForREST(url)
    if (myxml):
        achievement = TryGetNodes(myxml, "achievement")
        for i in range(0, len(achievement)):
            achievementId = TryGetNodeValues(achievement[i], "id")
            achievementName = TryGetNodeValues(achievement[i], "name")
            achievementText = TryGetNodeValues(achievement[i], "description")
            newAchievement = Achievement(achievementId[0], achievementName[0], achievementText[0])
            gAchievements[achievementId[0]] = newAchievement
        myxml.unlink()
        gAchievementsGenerated = 1


def GetAchievementsForUser(username, start, length):
    if (gAchievementsGenerated == 0):
        GenerateAchievementsList()
    url = AchievementsForUserURL(username, start, length)
    myxml = GetXMLForREST(url)
    achievements = []
    if (myxml):
        aId = TryGetNodeValues(myxml, "guid")  # you can extend this to get other nodes
        for i in range(0, len(aId)):
            achievement = gAchievements[aId[i]]
            achievements.append(achievement)
        myxml.unlink()
    return achievements


def GetProfileForUser(username):
    url = ProfileForUserURL(username)
    myxml = GetXMLForREST(url)
    if (myxml):
            image = TryGetNodeValues(myxml, "image")
            ext = image[0].split(".")
            FetchAndSave(image[0], username + "." + ext[len(ext) - 1])



############# SPORECASTS ##############
def GetAssetIdsForSporeCast(castId):
    url = AssetsForSporeCastURL(castId, 0, 5000)
    myxml = GetXMLForREST(url)
    ids = []
    if (myxml):
        assetids = TryGetNodes(myxml, "id")  # you can extend this to get other nodes
        for i in range(0, len(assetids)):
            ids.append(assetids[i])
        myxml.unlink()
    return ids


def GetAssetsForSporeCast(castId, start=0, length=5000):
    url = AssetsForSporeCastURL(castId, start, length)
    myxml = GetXMLForREST(url)
    if (myxml):
        assetids = TryGetNodes(myxml, "id")  # you can extend this to get other nodes
        for i in range(0, len(assetids)):
            FetchAndSaveSmallPNG(assetids[i].firstChild.nodeValue)
        myxml.unlink()


############# GLOBAL STATS ##############
def StatsAtTime():
    url = "http://www.spore.com/rest/stats"
    myxml = GetXMLForREST(url)
    num = []
    if (myxml):
        num = TryGetNodeValues(myxml, "totalUploads")
    return num[0]

