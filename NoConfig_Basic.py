import datetime
import threading
import customtkinter
from customtkinter import *
from PIL import Image
from tkinter import mainloop
import time
import requests

#Fetching quote using quote API -----
def get_quote():
    try: #if an errror occurs during API request it is caught

        API_HTML = ("https://api.api-ninjas.com/v1/quotes?category=inspirational") #Specify the location for the request to be made
        API_Response = requests.get(API_HTML, headers = {"X-Api-Key" : "XXXXXX"}) #Make the request using an API key

        ResponseBody = API_Response.json() #Convert repsosne to JSON format 
        Quote = ResponseBody[0]["quote"] #Fetch quote from JSON response

        Quote = Quote.split() #Split into words to check length for GUI
        if len(Quote) > 8 or len(Quote) < 5: #Is it too large?
            return get_quote() #Recursion
        return Quote #Return Quote if it meets size requirments
    
    except:
        return "Be the change that you wish to see in the world." #Default quote - Gandhi

def Get_IP_Location():
    try: #if an errror occurs during API request it is caught

        IpRequest = requests.get("https://api.ipify.org/?format=json") #Make the request using requests library to API web address specified
        Ip = IpRequest.json()["ip"] #Convert response to JSON

        IpDetail = requests.get(f"https://geo.ipify.org/api/v2/country,city?apiKey=XXXXX&ipAddress={Ip}")  #Repeat process using data gained above to gian further information
        IpDJson = IpDetail.json() #Convert response to JSON format
        return IpDJson["location"]["lat"],IpDJson["location"]["lng"], IpDJson["location"]["city"] #Return the data in list format
    
    except:
        return  [53.41667000, -2.25000000, "Manchester"] #Return by default the UK's best city

def Get_Weather_Data(lat,lng):
    try:
        WeatherRequest = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&appid=XXXXXXXX") #Make request to weather API using paramters
        WeatherData = WeatherRequest.json() #Convert response to JSON
        IconCode = WeatherData["weather"][0]["icon"] #Fetch current weather icon
        Temp = WeatherData["main"]["temp"]
        return {"Image_Path" : f"{IconCode}@2x.png",
                "Temp" : f"{Temp}°C"} #Return file path of image
    except:
        return {"Image_Path" : f"No_Wifi_Icon_Asset.png",
                "Temp" : f"N/A"} #Return universal no connection icon and message


#Get current time using datetime
def get_time():
    return datetime.datetime.now()


class App(customtkinter.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Location = Get_IP_Location()

        self.Weather_Data = Get_Weather_Data(self.Location[0],self.Location[1])
        self.StartTime = datetime.datetime.now()
        self.WeatherIcon = CTkImage(Image.open(self.Weather_Data["Image_Path"]), size = (70,70))

        self.CurrentTime = datetime.datetime.now()
        self.month = self.CurrentTime.strftime("%B")
        self.date = int(self.CurrentTime.strftime("%d"))
        self.geometry("500x500")
        #self.wm_attributes("-fullscreen", True)     
        #Widgets ---
        self.WeatherIconWidget = CTkLabel(master = self, text = "", image = self.WeatherIcon, font = ("Helvetica", 10, "bold"))
        self.LocationLabel = CTkLabel(master=self, text= self.Location[2], font = ("Modern No. 20", 15))
        self.TempLabel = CTkLabel(master=self, text= self.Weather_Data["Temp"] , font = ("Modern No. 20", 15, "bold"))
        self.TimeLabel = CTkLabel(master=self, text= self.CurrentTime.strftime("%H : %M %p"), font = ("Modern No. 20", 25, "bold"))
        self.DateLabel = CTkLabel(master = self, text= f"{self.month} {self.date} {self.Get_Date_Prefix(self.date)}", font = ("Modern No. 20", 20, "bold"))
        self.QuoteLabel = CTkLabel(master = self, text= "", font = ("Modern No. 20", 15,))
        self.GreetingLabel = CTkLabel(master=self, text= "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!", font = ("Helvetica Bold", 20, "bold"))

        self.TempLabel.place(x = 390, y = 40)
        self.WeatherIconWidget.place(x = 430, y = 15)
        self.LocationLabel.place(x = 435, y = 75)
        self.GreetingLabel.place(x = 180, y = 400)
        self.TimeLabel.place(x = 40, y = 40)
        self.DateLabel.place(x = 40, y = 80)
        self.QuoteLabel.place(x=140, y = 450)

    def Get_Date_Prefix(self,date):
        Prefixes = {1:"st", 2:"nd", 3:"rd"}
        if date % 10 in Prefixes.keys():
                return Prefixes[date%10]
        else:
                return "th"

    def update_time(self):
        self.CurrentTime = get_time()
        self.TimeLabel.configure(text = (self.CurrentTime).strftime("%H : %M %p"))
        time.sleep(1)
        self.update_time()

    def Update_Hour(self):
        self.Update_Weather()
        time.sleep(3600)


    def update_day(self):
        self.update_date()
        self.update_quote()
        self.update_greeting()
        time.sleep(86400)
        print("new day!")
        self.update_day()

    def update_greeting(self):
        self.QuoteLabel.configure(text = get_quote())

    def Update_Weather(self):
        self.Weather_Data = Get_Weather_Data(self.Location)
        self.WeatherDataLabel.configure(text = self.Weather_Data["Temp"], image = self.WeatherIcon )

    def update_date(self):
        self.CurrentTime = get_time()
        self.month = (self.CurrentTime).strftime("%B")
        self.date = int((self.CurrentTime).strftime("%d"))
        self.DateLabel.configure(text = f"{self.month} {self.date} {self.Get_Date_Prefix(self.date)}")


    def update_quote(self):
        self.QuoteLabel.configure(text = get_quote()) 




#Setting up the application envionment
app = App()
HourThread = threading.Thread(target = app.Update_Hour)
DayThread = threading.Thread(target = app.update_day)
TimeThread = threading.Thread(target = app.update_time)
DayThread.start()
TimeThread.start()
app.mainloop()

