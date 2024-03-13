import datetime
import threading
import customtkinter
from CTkListbox import *
from customtkinter import *
from PIL import Image
from tkinter import mainloop
import time
import requests



def Get_IP_Location():
    try: #if an errror occurs during API request it is caught

        IpRequest = requests.get("https://api.ipify.org/?format=json") #Make the request using requests library to API web address specified
        Ip = IpRequest.json()["ip"] #Convert response to JSON

        IpDetail = requests.get(f"https://geo.ipify.org/api/v2/country,city?apiKey=at_rkIIjN5RBwZwWPuowuM1aOH7NaMT9&ipAddress={Ip}")  #Repeat process using data gained above to gian further information
        IpDJson = IpDetail.json() #Convert response to JSON format
        return IpDJson["location"]["lat"],IpDJson["location"]["lng"], IpDJson["location"]["city"] #Return the data in list format
    
    except:
        return  [53.41667000, -2.25000000, "Manchester"] #Return by default the UK's best city


def Get_Weather_Data(lat, lng):
    try:
        WeatherRequest = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&appid=e1d3af16b36ac92b7b2c8988e5072359") #Make request to weather API using paramters
        WeatherData = WeatherRequest.json() #Convert response to JSON
        IconCode = WeatherData["weather"][0]["icon"] #Fetch current weather icon
        Temp = WeatherData["main"]["temp"]
        return {"Image_Path" : f"{IconCode}@2x.png",
                "Temp" : f"{Temp}°C"} #Return file path of image
    except:
        return {"Image_Path" : f"No_Wifi_Icon_Asset.png",
                "Temp" : f"N/A"} #Return universal no connection icon and message    

def Get_Date_Prefix(date):
        Prefixes = {1:"st", 2:"nd", 3:"rd"}
        print(date % 10)
        if date % 10 in Prefixes.keys() and date<3 and date>21:
                return Prefixes[date%10]
        else:
                return "th"

def get_quote():
    try: #if an errror occurs during API request it is caught

        API_HTML = ("https://api.api-ninjas.com/v1/quotes?category=inspirational") #Specify the location for the request to be made
        API_Response = requests.get(API_HTML, headers = {"X-Api-Key" : "BmpEwxYiqn0J4zBhTmA91g==OZT1qlY9q3QQJEuN"}) #Make the request using an API key

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

        IpDetail = requests.get(f"https://geo.ipify.org/api/v2/country,city?apiKey=at_rkIIjN5RBwZwWPuowuM1aOH7NaMT9&ipAddress={Ip}")  #Repeat process using data gained above to gian further information
        IpDJson = IpDetail.json() #Convert response to JSON format
        return IpDJson["location"]["lat"],IpDJson["location"]["lng"], IpDJson["location"]["city"] #Return the data in list format
    
    except:
        return  [53.41667000, -2.25000000, "Manchester"] #Return by default the UK's best city

def Get_Weather_Data(lat,lng):
    try:
        WeatherRequest = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&appid=e1d3af16b36ac92b7b2c8988e5072359") #Make request to weather API using paramters
        WeatherData = WeatherRequest.json() #Convert response to JSON
        print(WeatherData)
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




class App(customtkinter.CTk): #Class that is used for the main applicaiton window

    def __init__(self, *args, **kwargs): #Non-keyword and keyword arguments can be passed in, packed as dictionary
        super().__init__(*args, **kwargs) #Expand non-keyword and keyword dictionary into arguments 

        self.Current_News = ["Loading...", "Loading...", "Loading...", "Loading..."]
        
        self.Example_Reminders = ["Take the Dog for a walk",
                                "Jane's Birthday party - 3pm",
                                "Get shopping",
                                "Mow the grass"]
        
        self.Example_Timetable = ["09:00 - COMCORE1C Lecture",
                                "10:00 - COMCORE2C Lecture",
                                "13:00 - Dinner",
                                "14:35 - COMCORE1C Lecture"]

        self.Compliment = "You look nice!"
        self.Location = "Location"
        self.UppR_Widget = ""
        self.UppL_Widget = ""
        self.Centre_Widget = ""
        self.Bott_Centre_Widget = ""
        self.Current_Widgets = [self.UppL_Widget, self.UppR_Widget, self.Centre_Widget, self.Bott_Centre_Widget]
        self.User_Name = ""
        self.Location = Get_IP_Location()
        #Weather data and graphic ---------------
        self.WeatherIcon = CTkImage(Image.open("01d@2x.png"), size = (70,70)) #Store CTKimage object with argument as Image.open() method result store this in the WeatherIocn attribute
        

        #Time handling, storing of essential time and date informaiton ----------
        self.CurrentTime = datetime.datetime.now() 
        self.month = self.CurrentTime.strftime("%B")
        self.date = int(self.CurrentTime.strftime("%d"))

        self.Upp_Left("Time/Date")
        self.Upp_Right("N/A")
        self.Centre("Timetable")
        self.Bott_Centre("Time Greet")

        
        #self.wm_attributes("-fullscreen", True)     
        self.geometry("500x500")


    def Upp_Left(self,type):
        if type == "N/A":
            type =  ""
            self.Widget_Destroy(self.UppL_Widget)
        self.UppL_Widget = type  

        if type  == "Weather":
            self.WeatherWidget(60, 5)

        elif type == "Time/Date":
            self.TimeDate_Widget(20, 20)

        elif type == "Social":
            self.Social_Widget(40, 5)    

    def Upp_Right(self,type):
        if type == self.UppL_Widget:
            self.Widget_Destroy(self.UppL_Widget)
            self.UppL_Widget = ""
        
        self.Widget_Destroy(self.UppR_Widget)  
        if type == "N/A":
            self.UppR_Widget = ""
        else:
            self.UppR_Widget = type    


        if type  == "Weather":
            self.WeatherWidget(430, 5)

        elif type == "Time/Date":
            self.TimeDate_Widget(380, 20)

        elif type == "Social":
            self.Social_Widget(430, 5) 
        

    def Bott_Centre(self, type):
        if type == "N/A":
            if self.Bott_Centre != "":
                self.SubLabel.destroy()
                self.GreetingLabel.destroy()
            self.Bott_Centre_Widget = ""
            return 

        if self.Bott_Centre_Widget== "":
            self.SubLabel = CTkLabel(master = self, text= "Live as if you were to die tomorrow.", font = ("Modern No. 20", 15,), justify = CENTER)
            self.GreetingLabel = CTkLabel(master=self, font = ("Modern No. 20", 20, "bold"))
            self.GreetingLabel.place(x = 190, y = 420)
            self.SubLabel.place(x=130, y = 450)
        
        self.Greeting_Widget(type)
        self.Bott_Centre_Widget = type


    def Centre(self,type):
        if type == "N/A":
            if self.Centre_Widget != "":
                self.Widget_Destroy(self.Centre_Widget)
            self.Centre_Widget = ""
            return

        if self.Centre_Widget == "":
            self.List_Display = CTkListbox(self, width = 400, height = 150, border_width= 0,font = ("Modern No. 20", 3), justify="centre") #Using CTKListBox class an object is created and stored in the News_Display attribute
            self.List_Display._scrollbar.configure(width = 0) #Editting the objecgs attributes to acheve the desired look
            self.List_Display.place(x = 60, y= 130)

        self.Update_List_Widget(type)
        self.Centre_Widget = type
        

        


    def Widget_Destroy(self, type):
        if type == "Weather" :
            self.TempLabel.destroy()
            self.WeatherIconWidget.destroy()
            self.LocationLabel.destroy()
            
        elif type == "Time/Date":
            self.TimeLabel.destroy()
            self.DateLabel.destroy()

        elif type == "Social":
            self.MessageNotifLabel.destroy()
            self.SocialIcon.destroy()

        elif type == "Compliment":
            self.GreetingLabel.destroy()
            self.SubLabel.destroy()
        
        elif type in ["News", "Reminders", "Timetable"]:
            self.List_Display.destroy()

    def WeatherWidget(self,x,y):
            self.Weather_Data = Get_Weather_Data(self.Location[0], self.Location[1])
            self.WeatherIconWidget = CTkLabel(master = self, text = "", image = self.WeatherIcon)
            self.LocationLabel = CTkLabel(master=self, text= self.Location[2], font = ("Modern No. 20", 15))
            self.TempLabel = CTkLabel(master=self, text= "10°C", font = ("Modern No. 20", 15, "bold"))
        
            self.TempLabel.place(x = x-40, y = y+30)
            self.WeatherIconWidget.place(x = x, y = y)
            self.LocationLabel.place(x = x+5, y = y+55)
            print("Wetaher widget made")


    def Time_Greeting_Widget(self):
        self.GreetingLabel = CTkLabel(master=self, text= "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!", font = ("Modern No. 20", 20, "bold"))
        self.GreetingLabel.place(x = 190, y = 420)

    def Greeting_Widget(self, type):
        if type == "Compliment":
            self.GreetingLabel.configure(text = self.Compliment)

        elif type == "Time Greet" or type == "Compliment":
            self.GreetingLabel.configure(text = "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!" + self.User_Name + "!")
            self.GreetingLabel.place(x=170,y=420)


    def Social_Widget(self, x, y):

        PopUp = CTkInputDialog(text = "Enter Twitter Username:", title = "Twitter API")
        self.Twitter_Username = PopUp.get_input()

        PopUp = CTkInputDialog(text = "Enter Twitter Password:", title = "Twitter API")
        self.Twitter_Password = PopUp.get_input()

        self.SocialIcon = CTkLabel(master = self, text = "", image = CTkImage(Image.open("Twitter.png"), size = (50,50)))
        self.MessageNotifLabel = CTkLabel(master=self, text= "No messages", font = ("Modern No. 20", 15))

        self.MessageNotifLabel.place(x = x-10, y = y+55)
        self.SocialIcon.place(x = x+3, y = y+2)


    def TimeDate_Widget(self, x, y):
        self.TimeLabel = CTkLabel(master=self, text= self.CurrentTime.strftime("%H : %M %p"), font = ("Modern No. 20", 25, "bold"))
        self.DateLabel = CTkLabel(master = self, text= f"{self.month} {self.date} {Get_Date_Prefix(self.date)}", font = ("Modern No. 20", 20, "bold"))

        self.TimeLabel.place(x = x, y = y)
        self.DateLabel.place(x = x, y = y+40)

#Widget updating methods

    def Update_List_Widget(self, type):
        RGB = 192
        for i in range(4):
            RGB_Hex = (hex(RGB).replace('0x', '')).upper()
            RGB_Text_Colour = f"#{RGB_Hex}{RGB_Hex}{RGB_Hex}"
            RGB = RGB - 25
            
            if type == "News":
                    Val = self.Current_News[i].split()
                    print(Val)
            elif type == "Reminders":
                    
                    Val = self.Example_Reminders[i].split()
            elif type == "Timetable":
                    Val = self.Example_Timetable[i].split()

            if len(Val) > 4 and len("".join(Val)) > 20:
                Val = " ".join((Val[0:len(Val)//2] + ["\n"] + Val[len(Val)//2::]))
            self.List_Display.text_color = RGB_Text_Colour
            self.List_Display.insert(i,Val)
            self.List_Display.text_color = "Default"



    def Update_News(self):
        self.Current_News = []
        News_API_Response = requests.get("https://gnews.io/api/v4/top-headlines?category=general&max=4&lang=en&apikey=a0e5514835fad49b0ed972b0c14ec447")
        News_JSON = News_API_Response.json()
        for i in range(len(News_JSON["articles"])):
                Headline = News_JSON["articles"][i]["title"]

                Headline = Headline[0:Headline.index('-')] if '-' and "live:" in Headline else Headline

                self.Current_News.append(Headline)
        print(self.Current_News)

    def Update_Second(self):
        self.CurrentTime = get_time()
        if "Time/Date" in self.Current_Widgets:
            self.TimeLabel.configure(text = (self.CurrentTime).strftime("%H : %M %p"))
        time.sleep(1)
        self.Update_Second()

    def Update_Hour(self):
        Start_Time = None
        Start_Date = self.date
        while True:
            self.Current_Widgets = [self.UppL_Widget, self.UppR_Widget, self.Centre_Widget, self.Bott_Centre_Widget]
            if self.CurrentTime.strftime("%H") != Start_Time or Start_Time == None:
                print("hour updates")
                if "Weather" in  self.Current_Widgets:
                    self.Update_Weather()
                if "News" in self.Current_Widgets:
                    self.Update_News()
                    self.Update_List_Widget("News")
                if "Reminder" in self.Current_Widgets:
                    self.Update_Reminders()
                if "Time Greet" in self.Current_Widgets or "Personal Time Greet" in self.Current_Widgets:
                    self.Update_Greeting()
                    self.Update_Quote()
                Start_Time = self.CurrentTime.strftime("%H")
            if self.date != Start_Date or Start_Time == None:
                print("day updated")
                self.Update_Day()
            time.sleep(60)

    def Update_Day(self):
        self.Current_Widgets = [self.UppL_Widget, self.UppR_Widget, self.Centre_Widget, self.Bott_Centre_Widget]
        if "Time/Date" in  self.Current_Widgets:
            self.Update_Date()

        print(("Complement" in self.Current_Widgets or "Time Greet" in self.Current_Widgets or "Personal Time Greet" in self.Current_Widgets),self.Current_Widgets)
        if "Complement" in self.Current_Widgets or "Time Greet" in self.Current_Widgets or "Personal Time Greet" in self.Current_Widgets:
            self.Update_Quote()


    def Update_Reminders(self):
        return 

    def Update_Greeting(self):
        self.GreetingLabel.configure(text = "Good Morning" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon" + self.User_Name + "!")

    def Update_Weather(self):
        print(self.Location)
        self.Weather_Data = Get_Weather_Data(self.Location[0], self.Location[1])
        print(self.Weather_Data)
        self.TempLabel.configure(text = self.Weather_Data["Temp"])
        self.WeatherIcon.configure(image = self.WeatherIcon)

    def Update_Date(self):
        self.CurrentTime = get_time()
        self.month = (self.CurrentTime).strftime("%B")
        self.date = int((self.CurrentTime).strftime("%d"))
        self.DateLabel.configure(text = f"{self.month} {self.date} {Get_Date_Prefix(self.date)}")


    def Update_Quote(self):
        print("update quote")
        self.SubLabel.configure(text = get_quote())



#Setting up the application envionment
app = App()
#Bluetooth_Thread = threading.Thread(target = app.)
#Bluetooth_Thread.start()
HourThread = threading.Thread(target = app.Update_Hour)
TimeThread = threading.Thread(target = app.Update_Second)
HourThread.start()
TimeThread.start()
app.mainloop()
HourThread.join()
TimeThread.join()