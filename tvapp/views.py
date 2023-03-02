from django.shortcuts import render
import requests
from django.http import JsonResponse
from datetime import datetime
import pytz


def home(request):
    return render(request,'home.html')


def ajax(request):
    # localServerData = requests.get("http://192.168.1.16:8182/temp").json()
    # ebStatus = localServerData["EB_Status"]
    newYorkTz = pytz.timezone("Asia/Kolkata") 
    timeInNewYork = datetime.now(newYorkTz)
    currentTime = timeInNewYork.strftime("%-I:%M %p")
    currentDate = datetime.now().strftime("%d.%m.%Y")
    adminRoomTemp = 0
    adminRoomHum = 0
    greenRoomTemp = 0
    greenRoomHum = 0
    garageRoomTemp = 0
    garageRoomHum = 0
    try:
        a = requests.get("http://192.168.1.18:8182/temp").json() #static ip
    except:
        a = requests.get("http://192.168.1.18:8182/temp").json() # local ip

    for i in a:
        if i["room"] == "admin room":
            adminRoomTemp = i["temperature"]
            adminRoomHum = i["humidity"]

        if i["room"] == "green room":
            greenRoomTemp = i["temperature"]
            greenRoomHum = i["humidity"]

        if i["room"] == "garage":
            garageRoomTemp = i["temperature"]
            garageRoomHum = i["humidity"]
    context = {
        "currentTime": currentTime,
        "currentDate": currentDate,
        "adminRoomTemp": adminRoomTemp,
        "adminRoomHum": adminRoomHum,
        "greenRoomTemp": greenRoomTemp,
        "greenRoomHum": greenRoomHum,
        "garageRoomTemp": garageRoomTemp,
        "garageRoomHum": garageRoomHum
    }
    return JsonResponse(context)