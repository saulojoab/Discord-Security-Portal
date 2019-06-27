#coding: utf-8

import requests
import json

with open("credentials.json", encoding='utf-8-sig') as json_file:
    cred = json.load(json_file);

def addInfraction(userID, description, actionTaken):
    body = {
        "userID": userID,
        "description": description,
        "actionTaken": actionTaken
    }

    res = requests.post(cred["secretInsertUrl"], json=body);
    res = res.json();
    return res;

def getInfractions():
    res = requests.get("http://discord-security-api.herokuapp.com/infractions");
    return res.json();

def getUsers():
    res = requests.get("http://discord-security-api.herokuapp.com/users");
    return res.json();

def searchInfractions(userId):
    res = requests.get("http://discord-security-api.herokuapp.com/infractionsDiscordId?id=" + userId);
    return res.json();
