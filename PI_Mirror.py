
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
blusock.bind((MAC,PORT)) #Bind PI Mac address with port unused port number so that it can be idenitfied via a socket address
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

        API_Address = ("https://api.api-ninjas.com/v1/quotes?category=inspirational") #Specify the location for the request to be made
        API_Response = requests.get(API_Address, headers = {"X-Api-Key" : "BmpEwxYiqn0J4zBhTmA91g==OZT1qlY9q3QQJEuN"}) #Make the request using an API key

        ResponseBody = API_Response.json() #Convert response to JSON format 
        Quote = ResponseBody[0]["quote"] #Fetch quote from JSON response dictionary

        Quote = Quote.split() #Split into words to check length for GUI widget
        if len(Quote) > 8 or len(Quote) < 5: #Is it too large?
            return get_quote() #Use recursion to find another shorter quote
        return Quote #Return Quote as it meets size requirments
    
    except: #Run this block of code if an exception occurs
        return "Be the change that you wish to see in the world." #Default quote


def get_Compliment():
    try:
        Api_Address = ("https://8768zwfurd.execute-api.us-east-1.amazonaws.com/v1/compliments")
        API_Response = requests.get(Api_Address)
        return API_Response.json()
    except:
        return "You look nice today"

def get_time(): #This function will get the current time and return it used the datetime library
    return datetime.datetime.now()




#Class for the windows, this enables multiple instances of the windows to be created and cna be used in other scripts with ease

class App(customtkinter.CTk): #Class for the main application window

    def __init__(self, *args, **kwargs): #Constructor with Non-keyword and keyword arguments so they can be passed in, packed as dictionary
        super().__init__(*args, **kwargs) #Expand non-keyword and keyword dictionary into arguments and inherit atributes from superclass

        #----------------- Attributes ------------

        #Attributes storing defualt values, used to store data to be displayed in the center widget depending on the setting ---

        self.Current_News = ["Loading...", "Loading...", "Loading...", "Loading..."]

        self.Reminders = ["Take the Dog for a walk", 
                                "Jane's Birthday party - 3pm",
                                "Get shopping",
                                "Mow the grass"]
        
        self.Timetable = ["09:00 - COMCORE1C Lecture",
                                "10:00 - COMCORE2C Lecture",
                                "13:00 - Dinner",
                                "14:35 - COMCORE1C Lecture"]

        self.WeatherIcon = CTkImage(Image.open("01d@2x.png"), size = (100,100)) #Store CTKimage object with argument as Image.open() method result store this in the WeatherIocn attribute
        self.Compliment = "Loading Compliment..." 
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
        self.Bott_Centre("Compliment")

        self.title("Smart Mirror")
        #self.wm_attributes("-fullscreen", True)     
        self.geometry("700x1000")


    #Public class methods --------------------------

    # --- Widget Location methods, widget controller methods ----
        
    def Upp_Left(self,type): #Used to configure the upper left widget in the window
        if type == self.UppR_Widget:  #Use selection to check if this widget is the same as the one on the left if so then a swap should be made, only one instance of each widget is possible due to hardware limitations
            self.Widget_Destroy(self.UppR_Widget) #Delete the opposite sides widget
            self.UppR_Widget = "" #Update the opposite side widget attribute to confirm the swap
            
        self.Widget_Destroy(self.UppL_Widget) #Delete the last widget, there will alwyas be one there
        if type == "N/A" or type == "": #If the arugment passed in is "" or "N/A" specifying no widget
            self.UppL_Widget = "" #Update location widget attribute
        else:
            self.UppL_Widget = type #Update location widget attribute

        ''' Ideal switch case here, however due to python limitations elif required,
            this will handle the widget change by calling the related methods to create the widget instance specified in the functions arguments,
            each method call has the screen coordinates passed in as arguments, this leave room for project perfective maintenance adding further functionality'''
        

        if type  == "Weather":
            self.WeatherWidget(60, 5)

        elif type == "Time/Date":
            self.TimeDate_Widget(20, 20)

        elif type == "Social":
            self.Social_Widget(40, 5)    

    # ----- This method has the same functionality as the one above but for the opposite side -----
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

    def Bott_Centre(self, type): #Used to configure the bottom centre widget in the window
        if type == "" and self.Bott_Centre_Widget != "": #Check if the widget is to be deleted and if so has it alreayd been created?
            self.Widget_Destroy(self.Bott_Centre_Widget)#If a widget has been created that type "" must be for deletion of the widget
        else:
            self.Greeting_Widget(type) #A widget hasnt been create din this location before, therefore "" is for creation of the widget

        self.Bott_Centre_Widget = type #Update widget type location attribute

    def Centre(self,type): #This method has the same functionality as above but for a different location
        if type == "" and self.Centre_Widget != "":
            self.Widget_Destroy(self.Centre_Widget)
        else:
            self.Create_ListWidget() 
            self.Update_List_Widget(type)

        self.Centre_Widget = type 

    
    # --- Widget methods ----


    def Widget_Destroy(self, type): #Used to destroy a particular widget depedning ont he argument "type"
        #Uses selection ot identify the widget to be destoryed used the "destroy()"" method of the "customtkinter" class

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

        elif type in ["Compliment", "Time Greet", "Personal Time Greet"]: #Doesnt matter the type, saves memory
            self.GreetingLabel.destroy()
            self.SubLabel.destroy()
        
        elif type in ["News", "Reminders", "Timetable"]: #Doesnt matter the type, saves memory
            self.List_Display.destroy()


    #---- Widget creation methods takes screen coordinates as arguments ----

    def WeatherWidget(self,x,y):
            self.Weather_Data = Get_Weather_Data(self.Location[0], self.Location[1]) #Call the "Get_Weather_Data" function pass in the location attribute Longitude and Lattitude as parameters, store this in the "Weather_Data" attribute
            self.WeatherIconWidget = CTkLabel(master = self, text = "", image = self.WeatherIcon) #Creation of weather icon widget object using "CTkLabel()"" method
            self.LocationLabel = CTkLabel(master=self, text= self.Location[2], font = ("Poppins", 25)) #Creation of Location label using "CTkLabel()"" method
            self.TempLabel = CTkLabel(master=self, text= "10°C", font = ("Poppins", 20, "bold")) #Creation of temperature label using "CTkLabel()"" method
        
            #Place() the objects displaying them on the window in the specified coordinates
            self.TempLabel.place(x = x-90, y = y+38)
            self.WeatherIconWidget.place(x = x, y = y-10)
            self.LocationLabel.place(x = x-10, y = y+65)


    def Create_Greeting_Widget(self):
        self.GreetingLabel = CTkLabel(master=self, text= "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!", font = ("Poppins", 30, "bold")) #Creation of time greeting label using "CTkLabel()"" method, uses single line selection to decide what greetign to display
        self.GreetingLabel.place(relx=0.5, rely=0.95, anchor = "s") #Dispalying the greetingLabel object by anchroing it to a location ont he screen enablign it to flex due to dynamic length

    def Create_SubGreet_Widget(self):#Same functionality as the method above
        self.SubLabel = CTkLabel(master = self, text= "", font = ("Poppins", 25,))
        self.SubLabel.place(relx=0.5, rely=1, anchor = "s")

    def Create_ListWidget(self):
        self.List_Display = CTkListbox(self, width = 500, height = 300, border_width= 0,font = ("Poppins", 20), justify="centre") #Using CTKListBox class an object is created and stored in the News_Display attribute
        self.List_Display.font = customtkinter.CTkFont(customtkinter.ThemeManager.theme["CTkFont"]["family"],20) #Due to an error with the library, the font has been forcfible changed by accessing the objects attributes
        self.List_Display._scrollbar.configure(width = 0) #Editting the objects attributes to acheive the desired look as there is not a method offerign this functionality
        self.List_Display.place(relx=0.5, rely=0.6, anchor = "s") #Dispalying the greetingLabel object by anchroing it to a location ont he screen enablign it to flex due to dynamic length


    def Greeting_Widget(self, type): #Due to multiple options this method acts as a controller for the widget creation
        self.Create_Greeting_Widget() #Create the widget objects and display them using this method call
        self.Create_SubGreet_Widget() #Similar functiona;ity to the line above

        if type == "Compliment": #Use selection to decide which widget to configure dependant on "type" parameter value
            self.SubLabel.configure(text = self.Compliment) #Update greeting widget with the vlaue of the "Compliment" attribute


#MIGHT REMOVE -------------------------------------------------------------------
    def Social_Widget(self, x, y):
        self.SocialIcon = CTkLabel(master = self, text = "", image = CTkImage(Image.open("Twitter.png"), size = (50,50)))
        self.MessageNotifLabel = CTkLabel(master=self, text= "No messages", font = ("Poppins", 15))

        self.MessageNotifLabel.place(x = x-10, y = y+55)
        self.SocialIcon.place(x = x+3, y = y+2)


    def TimeDate_Widget(self, x, y):
        self.TimeLabel = CTkLabel(master=self, text= self.CurrentTime.strftime("%H : %M %p"), font = ("Poppins", 35, "bold")) #Creation of label object stored in "TimeLabel"
        self.DateLabel = CTkLabel(master = self, text= f"{self.month} {self.date} {Get_Date_Prefix(self.date)}", font = ("Poppins", 30, "bold")) #Creation of label object stored in "DateLabel"
        
        self.TimeLabel.place(x = x, y = y) #Display ob jects on widnow using "place()" method
        self.DateLabel.place(x = x, y = y+40)

#Widget updating methods


    def Update_Compliment(self):
        self.Compliment = get_Compliment()
        print(self.Compliment)
        self.SubLabel.configure(text = self.Compliment)


    def Update_List_Widget(self, type):
        RGB = 192 #Set initial RGB value, this will be the text colour of the first element
        for i in range(4): #Use for loop as only 4 items to be displayed due to screen space
            RGB_Hex = (hex(RGB).replace('0x', '')).upper()  #Convert RGB value to hex using hex() method
            RGB_Text_Colour = f"#{RGB_Hex}{RGB_Hex}{RGB_Hex}" #Convert to RGB format for changing text colour
            RGB = RGB - 25 #Decrement hex making it a lighter grey
            if type == "News": #Use selection to process the information accordingly
                    Val = self.Current_News[i].split()
            elif type == "Reminders":
                    Val = self.Reminders[i].split()
            elif type == "Timetable":
                    Val = self.Timetable[i].split()

            if len(Val) > 4 and len("".join(Val)) > 20: #Check length
                Val = " ".join((Val[0:len(Val)//2] + ["\n"] + Val[len(Val)//2::])) #Length too great so a breakline is added

            self.List_Display.text_color = RGB_Text_Colour #Set text colour to RGB value
            self.List_Display.insert(i,Val) #Insert item in location dictated by the for loop
        

    def Update_News(self): 
        self.Current_News = [] #Declare and initialise "Current_News" attribute
        News_API_Response = requests.get("https://gnews.io/api/v4/top-headlines?category=general&max=4&lang=en&apikey=a0e5514835fad49b0ed972b0c14ec447") #Make requests retreival to news api
        News_JSON = News_API_Response.json() #Convert JSON repsonse to dictionary
        for i in range(len(News_JSON["articles"])): #L
                
                Headline = News_JSON["articles"][i]["title"]
                print(Headline)
                Headline = Headline[0:Headline.index('-')] if '-' in Headline and "live:" in Headline else Headline

                self.Current_News.append(Headline)
        print(self.Current_News)

    def Update_Second(self):
        try: #This thread never joins therefore when the main tghread ends it crashes, this will prevent that forcing the thread to join
            while True: #Can't be recursive due to maximum recursion depth being reached

                self.CurrentTime = get_time() #Update attribute value with the current time
                if "Time/Date" in self.Current_Widgets: #Check if the widget exists as configuring would cause an error
                    self.TimeLabel.configure(text = (self.CurrentTime).strftime("%H : %M %p")) #Configure timelabel to display current time usingn the "strftime()" method
                time.sleep(1) #Pause thread execution for 1 second using "time()" thread
        except:
            return #If exception has occured return so the thread can be joined to the main thread
        

    def Update_Hour(self): 

        try:#Try except statement to prevent thread from crashing
            Start_Time = None #Set local variable start time to none
            Start_Date = self.date #Store the date the application has started in "Start_Date" attribute
            while True: #Due to recusrison depth limits a while True loop is required
                self.Current_Widgets = [self.UppL_Widget, self.UppR_Widget, self.Centre_Widget, self.Bott_Centre_Widget] #Update current widgets in case of change, avoids a crash
                if self.CurrentTime.strftime("%H") != Start_Time or Start_Time == None: #Use selection to check if the hour has changed or the applicaiton has just started

                    if "Weather" in  self.Current_Widgets: #Using selection update the necessary widgets by calling their respective update methods
                        self.Update_Weather()
                    if "News" in self.Current_Widgets:
                        self.Update_News()
                        self.Update_List_Widget("News")
                    if "Reminder" in self.Current_Widgets:
                        self.Update_Reminders()
                    if "Time Greet" in self.Current_Widgets or "Personal Time Greet" in self.Current_Widgets:
                        self.Update_Greeting()
                        self.Update_Quote()

                if self.date != Start_Date or Start_Time == None: #Check if the date has changed 
                    Start_Date = self.date #Update the start date
                    self.Update_Day() #Call this emthod to update the widgets that need daily updating

                Start_Time = self.CurrentTime.strftime("%H") #Update the start time
                time.sleep(60) #Sleep for a minute to save processor rescources
        except:
            return


    def Update_Day(self): #This method is caleld to update widgets that are required to be updated daily
        self.Current_Widgets = [self.UppL_Widget, self.UppR_Widget, self.Centre_Widget, self.Bott_Centre_Widget] #Update current widgets list attribute
        if "Time/Date" in  self.Current_Widgets: #Use selection to call the widgets respective updating  methods
            self.Update_Date()
        if "Compliment" in self.Current_Widgets:
            self.Update_Compliment()
        if "Time Greet" in self.Current_Widgets or "Personal Time Greet" in self.Current_Widgets:
            self.Update_Quote()


    def Update_Greeting(self): #This method is called to update the greeting widget
        self.GreetingLabel.configure(text = "Good Morning" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon" + self.User_Name + "!")


    def Update_Weather(self): #Method called to update weather widget
        self.Weather_Data = Get_Weather_Data(self.Location[0], self.Location[1]) #Call the "Get_Weather_Data()" method with the location attribute as arguments
        self.WeatherIcon_Path = self.Weather_Data["Image_Path"] #Fetch the weather icon path from the dictionry returned in the previous lines method call
        self.WeatherIcon = CTkImage(Image.open(self.WeatherIcon_Path), size = (100,100)) #Using "CTkImage()" method open the image specified by the image path
        self.TempLabel.configure(text = self.Weather_Data["Temp"]) #Update temperature label
        self.WeatherIconWidget.configure(image = self.WeatherIcon)  #Update and display the image object initialised above

    def Update_Date(self):
        self.CurrentTime = get_time() #Update "CurrentTime" attribute
        self.month = (self.CurrentTime).strftime("%B") #Slice the necessary information from the attribute
        self.date = int((self.CurrentTime).strftime("%d")) 
        self.DateLabel.configure(text = f"{self.month} {self.date} {Get_Date_Prefix(self.date)}") #Update the date using a formatted string


    def Update_Quote(self): 
        self.Quote = get_quote() #Update "Quote" attribute witht he return of "get_quote()" attribute
        self.SubLabel.configure(text = self.Quote) #Update "SubLabel" object text attribute

    def Update_Interface(self): #Called to update interface preference options
            global WifiConnection
            blusock.listen(1) #Allow one connection request
            while True: #Required to avoid recursion depth limit
                self.recvdata = [] 
                data = None

                device_Sock, device_Add = blusock.accept() #Store the connected device informatiom
                try: #Try except statemnt to avoid thread crashing if an exception occurs
                    data = device_Sock.recv(1024) #Receive 1024 bytes of data from the socket specified in the device_sock object
                    data = data.decode("UTF-8") #Decode data into unicode
                    data = data.split(",") #Sent by bluetooth client seperated via commas, breakdown the data received further converting it to a list format
                    Wifi_Login,Wifi_Pass,self.User_Name = data[4],data[5],data[6] #Update global variables and attributes with the data received 
                    if data[2] == "Timetable": #If a widget preference is Remidners or Tiemtable update their respective attributes
                        self.Timetable = data[7]
                    elif data[2] == "Reminders":
                        self.Reminders = data[7]


                    self.Current_Widgets = data[0:3] #Slice the data list from the start till third index and update the "Current_Widegts" attribute
                    self.Upp_Left(data[0]) #Update the interface by passing in the changes as arguments to the widget location methods
                    self.Upp_Right(data[1])
                    self.Centre(data[2])
                    self.Bott_Centre(data[3])

                except:
                    pass

                device_Sock.close() #Close the socket to void a resource leak

                if WifiConnection == False: #Chekc if boolean variable is False as this updated snd indicates a Wi-Fi connection
                    WifiJSON = open("Wifi_Det.json","r") #Open a json file, required so wifi connection information can be saved and be connected again
                    WifInfo = json.load(WifiJSON) #Convert JSON to python dictionary and store in local variable "WifiInfo"
                    WifiJSON.close() #Close file to avoid resource leak
                
                    if WifInfo["Wifi_Status"] == "False": #Manipulate dictionary updating it and reading it
                        WifInfo["Wifi_Log-In"] = Wifi_Login
                        WifInfo["Wifi_Pass"] = Wifi_Pass
                        WifInfo["Wifi_Status"] = "True"
                        WifiJSON = open("Wifi_Det.json","w") #Open JSON in write mode
                        WifiJSON.write(json.dumps(WifInfo,indent = 3)) #Update JSON with the manipulated dictionary 
                        WifiJSON.close() 
                        WifiConnection = Connect_Wifi() #Call the "Connect_Wifi" method to connect to the network information that ahs just been received

#Setting up the application envionment
app = App()
HourThread = threading.Thread(target = app.Update_Hour)
TimeThread = threading.Thread(target = app.Update_Second)
BlueThread= threading.Thread(target = app.Update_Interface)
BlueThread.start()
HourThread.start()
TimeThread.start()
app.mainloop()
HourThread.join()
TimeThread.join()