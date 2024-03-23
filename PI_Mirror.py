
import json,datetime,threading,customtkinter,os,time,requests,socket
from CTkListbox import *
from customtkinter import *
from PIL import Image
from tkinter import mainloop

customtkinter.set_appearance_mode("Dark") #Set window theme as "Dark" required to contrast mirror




#Global Variables ---------
WifiConnection = False 
MAC = "b8:27:eb:0d:66:5e"
PORT = 5
blusock = socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM,socket.BTPROTO_RFCOMM) #Global variable storing socket object for bluetooth communication
#blusock.bind((MAC,PORT)) #Bind PI Mac address with port unused port number so that it can be idenitfied via a socket address
Wifi_Login,Wifi_Pass = "","" #Global Wifi and Password variables s they can be accessed throughout




def Connect_Wifi(): #Function used to connect to a wireless network
    os.system("sudo" + " " +"iwconfig" + " "+ "wlan0" +" "+ "essid" + " " +Wifi_Login + " "+ "key" + " "+ Wifi_Pass) #Using the "os" library, admin terminal commands are executed to connect to the network witht he specified details 
    return True #Returns to confirm this has taken place, required to end the thread
    
def Get_IP_Location(): #This function is used to get the location of the users IP it returns this data as a list
    try: #if an errror occurs during the API requests it will be caught

        IpRequest = requests.get("https://api.ipify.org/?format=json") #Make the request using requests library to API web address specified, this reveals the users public address that the API returns
        Ip = IpRequest.json()["ip"] #Convert response to JSON

        IpDetail = requests.get(f"https://geo.ipify.org/api/v2/country,city?apiKey=at_rkIIjN5RBwZwWPuowuM1aOH7NaMT9&ipAddress={Ip}")  #Repeat process using data gained above to gain further information
        IpDJson = IpDetail.json() #Convert response to JSON format
        return IpDJson["location"]["lat"],IpDJson["location"]["lng"], IpDJson["location"]["city"] #Return the data in list format
    
    except: #Block of code to be executed if an exception occurs
        return  [53.41667000, -2.25000000, "Manchester"] #Return by default the UK's best city longitude and lattitude


def Get_Weather_Data(lat, lng): #Taking Lattiude and Longitude as parameters this function will return the weather data for that locaiton

    try: #Exception block used to catch exceptions oif the API request fails
        WeatherRequest = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&appid=e1d3af16b36ac92b7b2c8988e5072359") #Make request to weather API using parameters
        WeatherData = WeatherRequest.json() #Convert response to JSON
        IconCode = WeatherData["weather"][0]["icon"] #Using JSON response dictionary fetch the icon value
        Temp = WeatherData["main"]["temp"] # Repeat of abover however the temperature is fetched from the dictionary
        return {"Image_Path" : f"{IconCode}@2x.png", #return in a dictionary format the Icon value fetched with the file path postfixed at the end and the temperature
                "Temp" : f"{Temp}°C"}
    except: #Run this code if an exception is caught
        return {"Image_Path" : f"No_Wifi_Icon_Asset.png",
                "Temp" : f"N/A"} #Return universal no connection icon image path and message    

def Get_Date_Prefix(date): #function with date integer as paramter
        Postfixes = {1:"st", 2:"nd", 3:"rd"} #dictionary to store the string postfixes depdning on the number
        if date % 10 in Postfixes.keys() and date<3 and date>21: #selection divide the integer paramter value by 10 and check if the remainder is in the postfixes dictionary and if it is in the range of vlaues where a postfix is used
                return Postfixes[date%10] #exit function and return the prefix
        else:
                return "th" #return th as this is the postfix for all other values

def get_quote(): #Function to fetch the daily quote
    try: #if an errror occurs during API request it is caught, this also catches recursion depth errors which is a possibility due to thie nature of this function

        API_HTML = ("https://api.api-ninjas.com/v1/quotes?category=inspirational") #Specify the location for the request to be made
        API_Response = requests.get(API_HTML, headers = {"X-Api-Key" : "BmpEwxYiqn0J4zBhTmA91g==OZT1qlY9q3QQJEuN"}) #Make the request using an API key

        ResponseBody = API_Response.json() #Convert response to JSON format 
        Quote = ResponseBody[0]["quote"] #Fetch quote from JSON response dictionary

        Quote = Quote.split() #Split into words to check length for GUI widget
        if len(Quote) > 8 or len(Quote) < 5: #Is it too large?
            return get_quote() #Use recursion to find another shorter quote
        return Quote #Return Quote as it meets size requirments
    
    except: #Run this block of code if an exception occurs
        return "Be the change that you wish to see in the world." #Default quote

def get_time(): #This function will get the current time and return it used the datetime library
    return datetime.datetime.now()




#Class for the windows, this enables multiple instances of the windows to be created and cna be used in other scripts with ease

class App(customtkinter.CTk): #Class for the main application window

    def __init__(self, *args, **kwargs): #Constructor with Non-keyword and keyword arguments so they can be passed in, packed as dictionary
        super().__init__(*args, **kwargs) #Expand non-keyword and keyword dictionary into arguments and inherit atributes from superclass

        #----------------- Attributes ------------

        #Attributes storing defualt values, used to store data to be displayed in the center widget depednign on the setting ---

        self.Current_News = ["Loading...", "Loading...", "Loading...", "Loading..."]

        self.Example_Reminders = ["Take the Dog for a walk", 
                                "Jane's Birthday party - 3pm",
                                "Get shopping",
                                "Mow the grass"]
        
        self.Example_Timetable = ["09:00 - COMCORE1C Lecture",
                                "10:00 - COMCORE2C Lecture",
                                "13:00 - Dinner",
                                "14:35 - COMCORE1C Lecture"]

        self.WeatherIcon = CTkImage(Image.open("01d@2x.png"), size = (100,100)) #Store CTKimage object with argument as Image.open() method result store this in the WeatherIocn attribute
        self.Compliment = "You look nice!" #Default complement displayed in greeting label if used
        self.Location = "Loading..." #Used to store the users IP location under weather widget if used
        self.User_Name = ""
        self.Quote = "Loading Quote..."
        self.Location = Get_IP_Location()

        #Time handling, storing of essential time and date informaiton ----------
        self.CurrentTime = datetime.datetime.now() 
        self.month = self.CurrentTime.strftime("%B")
        self.date = int(self.CurrentTime.strftime("%d"))

        #Widget option attributes -------

        self.UppR_Widget = "" 
        self.UppL_Widget = ""
        self.Centre_Widget = ""
        self.Bott_Centre_Widget = ""
        self.Current_Widgets = [self.UppL_Widget, self.UppR_Widget, self.Centre_Widget, self.Bott_Centre_Widget]


        #Configuring window and widget settings
        self.Upp_Left("Time/Date")
        self.Upp_Right("Weather")
        self.Centre("News")
        self.Bott_Centre("Time Greet")

        self.title("Smart Mirror")
        #self.wm_attributes("-fullscreen", True)     
        self.geometry("700x1000")


    #Public class methods --------------------------


    def Upp_Left(self,type): #Used to configure the upper left widget in the window
        if type == self.UppR_Widget:  #Use selection to check if this widget is the same as the one on the left if so then a swap should be made, only one instance of each widget is possible due to hardware limitations
            self.Widget_Destroy(self.UppR_Widget)
            self.UppR_Widget = ""
            
        self.Widget_Destroy(self.UppL_Widget)  
        if type == "N/A" or type == "":
            self.UppL_Widget = ""
        else:
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
        if type == "N/A" or type == "":
            self.UppR_Widget = ""
        else:
            self.UppR_Widget = type    


        if type  == "Weather":
            self.WeatherWidget(484, 0)

        elif type == "Time/Date":
            self.TimeDate_Widget(380, 20)

        elif type == "Social":
            self.Social_Widget(484, 0) 
        

    def Bott_Centre(self, type):
        if type == "" and self.Bott_Centre_Widget != "":
            self.Widget_Destroy(self.Bott_Centre_Widget)
        else:
            self.Greeting_Widget(type)

        self.Bott_Centre_Widget = type

    def Centre(self,type):
        if type == "N/A" or type == "":
            if self.Centre_Widget != "":
                self.Widget_Destroy(self.Centre_Widget)
            self.Centre_Widget = ""
            return

        if self.Centre_Widget == "":
            self.List_Display = CTkListbox(self, width = 500, height = 300, border_width= 0,font = ("Poppins", 20), justify="centre") #Using CTKListBox class an object is created and stored in the News_Display attribute
            self.List_Display.font = customtkinter.CTkFont(customtkinter.ThemeManager.theme["CTkFont"]["family"],20)
            self.List_Display._scrollbar.configure(width = 0) #Editting the objecgs attributes to acheve the desired look
            self.List_Display.place(relx=0.5, rely=0.6, anchor = "s")

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

        elif type == "Compliment" or type == "Time Greet" or type == "Personal Time Greet":
            self.GreetingLabel.destroy()
            self.SubLabel.destroy()
        
        elif type in ["News", "Reminders", "Timetable"]:
            self.List_Display.destroy()

    def WeatherWidget(self,x,y):
            self.Weather_Data = Get_Weather_Data(self.Location[0], self.Location[1])
            self.WeatherIconWidget = CTkLabel(master = self, text = "", image = self.WeatherIcon)
            self.LocationLabel = CTkLabel(master=self, text= self.Location[2], font = ("Poppins", 25))
            self.TempLabel = CTkLabel(master=self, text= "10°C", font = ("Poppins", 20, "bold"))
        
            self.TempLabel.place(x = x-90, y = y+38)
            self.WeatherIconWidget.place(x = x, y = y-10)
            self.LocationLabel.place(x = x-10, y = y+65)
            print("Wetaher widget made")


    def Create_Greeting_Widget(self):
        self.GreetingLabel = CTkLabel(master=self, text= "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!", font = ("Poppins", 30, "bold"))
        self.GreetingLabel.place(relx=0.5, rely=0.95, anchor = "s")

    def Create_Quote_Widget(self):
        self.SubLabel = CTkLabel(master = self, text= self.Quote, font = ("Poppins", 25,))
        #self.SubLabel.place(x=204, y = 945)
        self.SubLabel.place(relx=0.5, rely=1, anchor = "s")

    def Greeting_Widget(self, type):
        self.Create_Greeting_Widget()
        self.Create_Quote_Widget()
        if type == "Compliment":
            self.GreetingLabel.configure(text = self.Compliment)

        elif type == "Time Greet" or type == "Personal Time Greet":
            self.GreetingLabel.configure(text = "Good Morning" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon" + self.User_Name + "!")



    def Social_Widget(self, x, y):

        PopUp = CTkInputDialog(text = "Enter Twitter Username:", title = "Twitter API")
        self.Twitter_Username = PopUp.get_input()

        PopUp = CTkInputDialog(text = "Enter Twitter Password:", title = "Twitter API")
        self.Twitter_Password = PopUp.get_input()

        self.SocialIcon = CTkLabel(master = self, text = "", image = CTkImage(Image.open("Twitter.png"), size = (50,50)))
        self.MessageNotifLabel = CTkLabel(master=self, text= "No messages", font = ("Poppins", 15))

        self.MessageNotifLabel.place(x = x-10, y = y+55)
        self.SocialIcon.place(x = x+3, y = y+2)


    def TimeDate_Widget(self, x, y):
        self.TimeLabel = CTkLabel(master=self, text= self.CurrentTime.strftime("%H : %M %p"), font = ("Poppins", 35, "bold"))
        self.DateLabel = CTkLabel(master = self, text= f"{self.month} {self.date} {Get_Date_Prefix(self.date)}", font = ("Poppins", 30, "bold"))
        
        self.TimeLabel.place(x = x, y = y)
        self.DateLabel.place(x = x, y = y+40)

#Widget updating methods

    def Update_List_Widget(self, type):
        RGB = 192
        for i in range(4):
            RGB_Hex = (hex(RGB).replace('0x', '')).upper()
            RGB_Text_Colour = f"#{RGB_Hex}{RGB_Hex}{RGB_Hex}"
            RGB = RGB - 25
            print(type)
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
            self.List_Display.font_size = 15
            self.List_Display.insert(i,Val)
            self.List_Display.text_color = "Default"
        



    def Update_News(self):
        self.Current_News = []
        News_API_Response = requests.get("https://gnews.io/api/v4/top-headlines?category=general&max=4&lang=en&apikey=a0e5514835fad49b0ed972b0c14ec447")
        News_JSON = News_API_Response.json()
        for i in range(len(News_JSON["articles"])):
                Headline = News_JSON["articles"][i]["title"]
                print(Headline)
                Headline = Headline[0:Headline.index('-')] if '-' in Headline and "live:" in Headline else Headline

                self.Current_News.append(Headline)
        print(self.Current_News)

    def Update_Second(self):
        try: #This thread never joins therefore when the main tghread ends it crashes, this will prevent that forcing the thread to join
            while True: #Can't be recursive due to maximum recursion depth being reached

                self.CurrentTime = get_time()
                if "Time/Date" in self.Current_Widgets:
                    self.TimeLabel.configure(text = (self.CurrentTime).strftime("%H : %M %p"))
                time.sleep(1) 
        except:
            return
        
    def Update_Hour(self):
        try:
            Start_Time = None
            Start_Date = self.date
            while True:
                self.Current_Widgets = [self.UppL_Widget, self.UppR_Widget, self.Centre_Widget, self.Bott_Centre_Widget]
                if self.CurrentTime.strftime("%H") != Start_Time or Start_Time == None:
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
        except:
            return

    def Update_Day(self):
        self.Current_Widgets = [self.UppL_Widget, self.UppR_Widget, self.Centre_Widget, self.Bott_Centre_Widget]
        if "Time/Date" in  self.Current_Widgets:
            self.Update_Date()

        if "Complement" in self.Current_Widgets or "Time Greet" in self.Current_Widgets or "Personal Time Greet" in self.Current_Widgets:
            self.Update_Quote()


    def Update_Reminders(self):
        return 

    def Update_Greeting(self):
        self.GreetingLabel.configure(text = "Good Morning" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon" + self.User_Name + "!")

    def Update_Weather(self):
        print(self.Location)
        self.Weather_Data = Get_Weather_Data(self.Location[0], self.Location[1])
        self.WeatherIcon_Path = self.Weather_Data["Image_Path"]
        self.WeatherIcon = CTkImage(Image.open(self.WeatherIcon_Path), size = (100,100))
        self.TempLabel.configure(text = self.Weather_Data["Temp"])
        self.WeatherIconWidget.configure(image = self.WeatherIcon)

    def Update_Date(self):
        self.CurrentTime = get_time()
        self.month = (self.CurrentTime).strftime("%B")
        self.date = int((self.CurrentTime).strftime("%d"))
        self.DateLabel.configure(text = f"{self.month} {self.date} {Get_Date_Prefix(self.date)}")


    def Update_Quote(self):
        self.Quote = get_quote()
        print(self.Quote)
        self.SubLabel.configure(text = self.Quote)

    def Update_Interface(self):
            global WifiConnection
            print("BlueThread")
            blusock.listen(1)
            while True:
                self.recvdata = []
                data = None
            #try:
    
                device_Sock, device_Add = blusock.accept()
                try:
            
                    print("Connection accepted",device_Sock,"end")
                    data = device_Sock.recv(1024)
                    data = data.decode("UTF-8")
                    data = data.split(",")
                    print(data)
                    Wifi_Login,Wifi_Pass,self.User_Name = data[4],data[5],data[6]
                    print(self.Current_Widgets)
                    self.Current_Widgets = data[0:3]
                    self.Upp_Left(data[0])
                    self.Upp_Right(data[1])
                    self.Centre(data[2])
                    self.Bott_Centre(data[3])
                except:
                    pass
                    print("except")
                device_Sock.close()

                if WifiConnection == False:
                    WifiJSON = open("Wifi_Det.json","r")
                    WifInfo = json.load(WifiJSON)
                    WifiJSON.close()
                
                    if WifInfo["Wifi_Status"] == "False":
                        WifInfo["Wifi_Log-In"] = Wifi_Login
                        WifInfo["Wifi_Pass"] = Wifi_Pass
                        WifInfo["Wifi_Status"] = "True"
                        WifiJSON = open("Wifi_Det.json","w")
                        WifiJSON.write(json.dumps(WifInfo,indent = 3))
                        WifiJSON.close()
                        WifiConnection = Connect_Wifi()
    
    

        #Keep listneing on socket untildata received
        #if data received
        #Update widgets

#Setting up the application envionment
app = App()
#Bluetooth_Thread = threading.Thread(target = app.)
#Bluetooth_Thread.start()
HourThread = threading.Thread(target = app.Update_Hour)
TimeThread = threading.Thread(target = app.Update_Second)
BlueThread= threading.Thread(target = app.Update_Interface)
BlueThread.start()
HourThread.start()
TimeThread.start()
app.mainloop()
HourThread.join()
TimeThread.join()