from django.shortcuts import render
import requests
from django.http import JsonResponse
# Create your views here.

def home(request):
    return render(request,'home.html')


def ajax(request):
    # localServerData = requests.get("http://192.168.1.16:8182/temp").json()
    # ebStatus = localServerData["EB_Status"]
    adminRoomTemp = 0
    adminRoomHum = 0
    greenRoomTemp = 0
    greenRoomHum = 0
    garageRoomTemp = 0
    garageRoomHum = 0
    try:
        a = requests.get("http://192.168.1.16:8182/temp").json() #static ip
    except:
        a = requests.get("http://192.168.1.16:8182/temp").json() # local ip

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
        "adminRoomTemp": adminRoomTemp,
        "adminRoomHum": adminRoomHum,
        "greenRoomTemp": greenRoomTemp,
        "greenRoomHum": greenRoomHum,
        "garageRoomTemp": garageRoomTemp,
        "garageRoomHum": garageRoomHum
    }
    print(context)
    return JsonResponse(context)