from django.shortcuts import render
from django.http import JsonResponse
import pytz
import requests
import pyrebase
from datetime import datetime

config = {
    "apiKey": "AIzaSyCCTeiCYTB_npcWKKxl-Oj0StQLTmaFOaE",
    "authDomain": "marketing-data-d141d.firebaseapp.com",
    "databaseURL": "https://marketing-data-d141d-default-rtdb.firebaseio.com/",
    "storageBucket": "marketing-data-d141d.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def home(request):
    return render(request,'home.html')


def ajax(request):
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
    quotationCount = 0
    invoiceCount = 0
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
    quote = db.child("QuotationAndInvoice").get().val()
    tm = datetime.now()
    thisYear = tm.strftime("%Y")
    thisMonth = tm.strftime("%m")
    for i in quote:
        if i == "QUOTATION":
            try:
                for q in quote[i][thisYear][thisMonth]:
                    quotationCount += 1
            except:
                pass
        if i == "INVOICE":
            try:
                for q in quote[i][thisYear][thisMonth]:
                    invoiceCount += 1
            except:
                pass

    context = {
        "currentTime": currentTime,
        "currentDate": currentDate,
        "adminRoomTemp": adminRoomTemp,
        "adminRoomHum": adminRoomHum,
        "greenRoomTemp": greenRoomTemp,
        "greenRoomHum": greenRoomHum,
        "garageRoomTemp": garageRoomTemp,
        "garageRoomHum": garageRoomHum,
        "quotationCount": quotationCount,
        "invoiceCount": invoiceCount,
    }
    return JsonResponse(context)