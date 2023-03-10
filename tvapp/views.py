from django.shortcuts import render
from django.http import JsonResponse
import pytz
import requests
import pyrebase
from datetime import date,datetime

Config = {
  "apiKey": "AIzaSyAFzuEn-ONlGoqsnvICugiotQe0nT9Ge48",
  "authDomain": "admin-13fa8.firebaseapp.com",
  "databaseURL": "https://admin-13fa8-default-rtdb.firebaseio.com",
  "projectId": "admin-13fa8",
  "storageBucket": "admin-13fa8.appspot.com",
  "messagingSenderId": "147393646122",
  "appId": "1:147393646122:web:f0b5abd0836275dbcfbd53",
  "measurementId": "G-8QYG0NH18C"
}

firebase = pyrebase.initialize_app(Config)
db = firebase.database()


def home(request):
    time= datetime.now().strftime("%X%p")
    curr_day = datetime.now().strftime("%d")
    curr_mon_year = datetime.now().strftime("%Y-%m")
    curr_year = datetime.now().strftime("%Y")
    curr_month = datetime.now().strftime("%m")
    curr_date1=datetime.now().strftime("%Y-%m-%d")
    curr_monthname=datetime.now().strftime("%B")
    curr_day=str(curr_day)
    curr_mon_year=str(curr_mon_year)
    curr_mon=str(curr_month) 
    curr_year=str(curr_year)
    curr_date=str(curr_date1)

    newleads=db.child("customer").get().val()
    count=0
    for num in newleads:
        month1=newleads[num]["created_date"]
        monthandyear=month1[0:7]
        if monthandyear == curr_mon_year:
            dayfromdb = monthandyear[8:10]
            if curr_day <= '15':
                if dayfromdb <= '15':
                    count=count+1 
                    half=True
            else:
                if dayfromdb >= '16':
                    count=count+1
                    half=False
    newleads=count
    half=half

    totalpoints=[]
    prpoints=db.child("PRPoints").get().val()
    for uid in prpoints:
        for year in prpoints[uid]:
            if  year == curr_year:
                for date in prpoints[uid][year][curr_mon]:
                    totalpoints.append(prpoints[uid][year][curr_mon][date]['points'])
    for i in range(0, len(totalpoints)):
        totalpoints[i] = int(totalpoints[i])
    totalpoints=sum(totalpoints)
    
    QuotationAndInvoice=db.child("QuotationAndInvoice").get().val()
    invoicecount=0
    for data1 in QuotationAndInvoice['INVOICE'][curr_year][curr_mon]:
        invoicecount=invoicecount+1
    quotationcount=1
    for data1 in QuotationAndInvoice['QUOTATION'][curr_year][curr_mon]:
        quotationcount=quotationcount+1
    staff=db.child("staff").get().val()
    staffnamelist=[]
    for userid in staff:
        if staff[userid]['department'] == 'PR':
            staffnamelist.append(staff[userid]['name'])
    return render(request,'home.html',{'newleads':newleads,'half':half,'totalpoints':totalpoints,'monthname':curr_monthname,
    'currentdate':curr_date1,'time':time,'quotationcount':quotationcount,'invoicecount':invoicecount,'staffnamelist':staffnamelist})

def ajax(request):
    asiaTime = pytz.timezone("Asia/Kolkata")
    asiaTime = datetime.now(asiaTime)
    currentTime =  asiaTime.strftime("%I:%M:%S %p")
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
        if i["room"] == "Admin Room":
            adminRoomTemp = i["temperature"]
            adminRoomHum = i["humidity"]

        if i["room"] == "Green Room":
            greenRoomTemp = i["temperature"]
            greenRoomHum = i["humidity"]

        if i["room"] == "Garage":
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
    