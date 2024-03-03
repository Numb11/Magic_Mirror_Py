import requests
import os

def Get_IP_Location():
    try:
        IpRequest = requests.get("https://api.ipify.org/?format=json")
        Ip = IpRequest.json()["ip"]

        IpDetail = requests.get(f"https://geo.ipify.org/api/v2/country,city?apiKey=at_rkIIjN5RBwZwWPuowuM1aOH7NaMT9&ipAddress={Ip}")
        IpDJson = IpDetail.json()
        return IpDJson["location"]["lat"],IpDJson["location"]["lng"], IpDJson["location"]["city"]
    
    except:
        return  [53.41667000, -2.25000000, "Manchester"] #Return by default UK's best city

def Get_Weather_Icon(lat,lng):
    try:
        WeatherRequest = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid=e1d3af16b36ac92b7b2c8988e5072359") #Make request to weather API using paramters
        WeatherData = WeatherRequest.json() #Convert response to JSON
        IconCode = WeatherData["weather"][0]["icon"] #Fetch current weather icon
        return f"https://openweathermap.org/img/wn/{IconCode}@2x.png" #Return address of image
    except:
        return "https://th.bing.com/th/id/R.a1450ef402eed26d20e536882cd418ad?rik=nbaeBawDwedggg&riu=http%3a%2f%2fclipart-library.com%2fimg%2f2094903.png&ehk=q5welI68e7M2HUrurkp5tStoGpYJwSDvAXJq0btcTok%3d&risl=&pid=ImgRaw&r=0" #Return universal no connection icon

print(Get_Weather_Icon(53.4115,-2.83935))