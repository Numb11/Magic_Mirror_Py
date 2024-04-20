#COnfiguration application to run on a windows machine communicating to the mirror via a bluetooth connection median

#Libraries --------
from CTkListbox import *
from CTkMessagebox import *
from customtkinter import *
from PIL import Image
import subprocess, threading,socket, datetime, customtkinter



def caesur(plaintext,shift): #Function used to encrypt data passed in as argumet by the shift va;ue passed in
    encrypted = []     #Local varibale declaration
    for i in plaintext: #For loop to loop through each character of the plaintext
        encrypted.append(chr(ord(chr(ord(i)+shift))+shift)) #Append the encrypted list with the character shifted by the specified amount in the alphabet
    encrypted = "".join(encrypted) #Convert the encrypted list to a string by joining the values by whitespace
    return encrypted #Return the encrypted data

#Global Variables -----------------
WifiSelectionWin = None 
PIMACAddress = "b8:27:eb:0d:66:5e"
PORT = 4
Wifi_User, Wifi_Pass = "","" #Global Wifi and Password variables, they can be accessed throughout
Pi_WifiStatus = False
Data_Sent_Stat = False

def Send_Pi_Data(UL,UR,BCENT,CENT, User_Name,TbleRmdInfo,name): #Function called to send data to the mirror, it requires the widgets names being used to be passed in as arguments
    global Wifi_User, Wifi_Pass, Data_Sent_Stat #Not passed in due to them being updated in seperate thread after the call
    try: #Requiered to prevent thread crashing
            BlueSock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) #Local variable storing socket object for bluetooth communication
            BlueSock.connect((PIMACAddress, PORT)) #Call connect() method on socket passing in the global variables PIMACAddress and PORT as arguments
            BlueSock.send(bytes((UL+","+UR+","+BCENT+","+CENT+","+Wifi_User+","+Wifi_Pass+","+"/".join(TbleRmdInfo)+","+User_Name), "UTF-8")) #Use send() method with the relevant data converted to bytes using the byts() method
            print((UL+","+UR+","+BCENT+","+CENT+","+Wifi_User+","+Wifi_Pass+","+"/".join(TbleRmdInfo)+","+User_Name).split(","))
            BlueSock.close() #Close the socket to avoid rescource leak
            Data_Sent_Stat = True #Update Data_Sent_Stat so the UI cna be updated appropriately
            
    except:
            BlueSock.close() #Close the socket to avoid rescource leak
            Data_Sent_Stat = False #Update Data_Sent_Stat so the UI can be updated appropriately
    return

def Get_Near_NetworksName(): #Function used to find nearby networks
    ConnectionSSIDs = [] #Local list variable to store the SSID name of each network 
    print("running")
    try: #Try except message requires to avoid thread crash
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'networks']) #Using subprcoess library, make temrinal command to get nearby networks
        print(result)
        result = result.decode("utf-8").split("\n") #Remove break lines and cast bresponse into list so that thedata can be read and manipulated easietr
        print(result)
        result = list(filter(lambda x: "SSID" in x,result)) #Using filtfer command and lambda, filter any data that is not the SSID name in the result
        for i in result: #Loop through each value in the resulty list
            ConnectionSSIDs.append(i.split(":")[1][1:-1].strip()) #Strip white space and irrelevamt data from value then append this to the ConnectionSSIDs lsit

    except: #Run the block of code below if an exception is caught
        ConnectionSSIDs.append("Absent") #Add the string "Absent" to the ConnectionSSIDs list so the program can acr accordingly
    return ConnectionSSIDs #Return the Netword SSID name
    
def Get_NetworkPass(network_name): #This function is used to get the passwprd of the network SSID passed in
    Network_pass = "" #Declare and initialise Network_pass local variable
    try: #Requires to avoid thread crash as this fucntion will be called in a seperate thread
        result = subprocess.check_output(["netsh",  "wlan", "show", "profile", network_name, "key", "=", "clear"]) #Using the subprocess class, a windows temrinak command is ran requesting the password for the SSID, requires the user has signed into the network in the past
        result = result.decode().split("\n") #Remove break line characters and cast result into a list
        result = list(filter(lambda x: "Key Content" in x,result)) #Filter result so only the SSID key remains
        for i in result: #Loop through the results values
            Network_pass= (i.split(":")[1]).strip() #Split the value by ":" which si what each key us seperated by, and remove the white space using the strip() method
            if "b'Profile" in Network_pass.split(): #Check if the password is available
                Network_pass = None #Required so the UI can update accordingly
    except:
        Network_pass = None

    return Network_pass #Return the password exiting out of the function












class WifiSelection(CTkToplevel): # Creation of another window used for the the inputting of wifi credentials
    def __init__(self, *args, **kwargs): #Non-keyword and keyword arguments can be passed in, packed as dictionary
        super().__init__(*args, **kwargs) #Expand non-keyword and keyword dictionary into arguments 
        self.Label = CTkLabel(self,text = "Please choose the network you want \n the mirror to connect to:",font = ("Arial", 15))
        self.Wifi_Selection = CTkListbox(self, width = 400, height = 150, border_width= 0,font = ("Arial", 15), justify="centre", command = self.get_password) #Using CTKListBox class an object is created and stored in the News_Display attribute
        #Widget placements relative to screen coordinates ----

        self.Wifi_Selection.place(x=70, y = 100) 
        self.Label.place(x=120,y=40)

        self.geometry("500x500") #Specify window saize by pixels
        self.Update_ConnectionsList(Get_Near_NetworksName()) #Get nearby networks and store their SSIDs in the Update_ConnectionsList attribute

    def Update_ConnectionsList(self,values): #Method used to update the Wifi_Selection listbox widget
        RGB = 192 #Starting RGB value for text colour
        for i in range(len(values)): #Loop through the values parameter
            RGB_Hex = (hex(RGB).replace('0x', '')).upper() #Convertr RGB integer to HEX, which is required for colouring the text
            RGB_Text_Colour = f"#{RGB_Hex}{RGB_Hex}{RGB_Hex}" 
            RGB = RGB - 10 #Decrement the RGB value
            
            Val = values[i].split() #Split the values and select the index specified by i

            Val = " ".join((Val[0:len(Val)//2] + ["\n"] + Val[len(Val)//2::])) #Add a break line chacter in the middle of the string value
            self.Wifi_Selection.text_color = RGB_Text_Colour #Cgange text colour attribute of the Wifi_Selection object
            self.Wifi_Selection.insert(i,Val) #Append the value to the widget object stored in Wifi_Selection
            self.Wifi_Selection.text_color = "Default" #Return text value to system default




    def get_password(self,SSID): #Method used to get the wifi password and update the UI accordingly
        global Wifi_User,Wifi_Pass,WifiSelectionWin #Define variables as global
        SSID = SSID.strip() #Rempve whitespace from SSID parameter value
        NetworkPass = Get_NetworkPass(SSID) #Store the return reuslt of the Get_NetworkPass() method with the SSID paramter
        if NetworkPass == None: #If a network password is not able to be fetched
            CTkMessagebox(title="Connection error", message="Failure to connect, please move device closer and try again", icon="warning") #Display a failure message to the user using the CTkMessageBox object
            self.Button = CTkButton(self, text = "Continue with Bluetooth", command = self.SendData) #Create a button widget offfering the option to continue with bluetooth communication
            
            self.Button.place(x=155, y=400) #Place the widget in the screen coordinates specified
        else: #If a network password has been fetched the block of code below is processed
            #Rewrite the wifi status in "Status.txt"
            Wifi_StatusF = open("Status.txt", "w") 
            Wifi_StatusF.write("Wifi-Status = True")
            Wifi_StatusF.close() #Close the file to avoid resource leak
            Wifi_User = SSID #Update global variable, Wifi_User
            Wifi_Pass = NetworkPass #Initalise globla vairbale Wifi_Pass with NetworkPass
            CTkMessagebox(title="Succcessful connection", message="Device connected!", icon="check") #Display success message using CTkMessagebox class
            self.SendData()


    def SendData(self): #This method is called when the continue with bluetooth button is pressed
        global Pi_WifiStatus,WifiSelectionWin #Define variables as global
        WifiSelectionWin = None #Update global variable WifiSelectionWin to None so that it can be checked when creating another window, avoids crashing
        Pi_WifiStatus = True
        self.destroy() #The window is closed and the instance destoryed using the close() method









class App(customtkinter.CTk): #Class that is used for the main applicaiton window

    def __init__(self, *args, **kwargs): #Non-keyword and keyword arguments can be passed in, packed as dictionary
        super().__init__(*args, **kwargs) #Expand non-keyword and keyword dictionary into arguments 

        #Attribute stores example data to simulate the mirror's interface
        self.Example_News = ["More lives lost than saved in Troubles due to British spy, report finds",
                                "Justin Welby says he carries personal alarm amid increasing threats in church",
                                "Head of UK science body calls for ‘creative disagreement’ after Michelle Donelan libel row",
                                "BP claws back £1.8m from sacked boss Looney and hands new CEO £8m pay deal"] 
        

        self.Example_Complement = "You look nice!"
        self.Location = "Location"
        #Screen location widget attributes
        self.UppR_Widget = ""
        self.UppL_Widget = ""
        self.Centre_Widget = ""
        self.Bott_Centre_Widget = ""
        self.Sub_Butt_Stat = False
        self.User_Name = ""
        self.Tble_RmdInfo = ""
        self.title("Widget Customiser")

        #Weather data and graphic ---------------
        self.WeatherIcon = CTkImage(Image.open("01d@2x.png"), size = (70,70)) #Store CTKimage object with argument as Image.open() method result store this in the WeatherIocn attribute
        

        #Time handling, storing of essential time and date informaiton ----------
        self.CurrentTime = datetime.datetime.now() 
        self.month = self.CurrentTime.strftime("%B")
        self.date = int(self.CurrentTime.strftime("%d"))

        #Declaration of multi choice widget object attributes

        self.Upp_Right_Combo = CTkOptionMenu(master = self,
                                                            values =["Weather", "Time/Date", "Social", "N/A"],
                                                            command = self.Upp_Right,
                                                            width = 35,
                                                            fg_color = "#53595D",
                                                            button_color = "#53595D",
                                                            corner_radius = 10,
                                                            font = ("Arial", 15),
                                                            dropdown_font = ("Arial", 15),
                                                            dropdown_fg_color = "#727682",)
        
        self.Upp_Left_Combo = CTkOptionMenu(master = self,
                                                            values =["Weather", "Time/Date", "Social", "N/A"],
                                                            command = self.Upp_Left,
                                                            width = 35,
                                                            fg_color = "#53595D",
                                                            button_color = "#53595D",
                                                            corner_radius = 10,
                                                            font = ("Arial", 15),
                                                            dropdown_font = ("Arial", 15),
                                                            dropdown_fg_color = "#727682",)
        
        self.Centre_Combo = CTkOptionMenu(master = self,
                                                            values =["News", "Reminders", "Timetable", "N/A"],
                                                            command = self.Centre,
                                                            width = 35,
                                                            fg_color = "#53595D",
                                                            button_color = "#53595D",
                                                            corner_radius = 10,
                                                            font = ("Arial", 15),
                                                            dropdown_font = ("Arial", 15),
                                                            dropdown_fg_color = "#727682",)
        

        self.BCentre_Combo = CTkOptionMenu(master = self,
                                                            values =["Complement", "Time Greet", "Personal Time Greet","N/A"],
                                                            command = self.Bott_Centre,
                                                            width = 35,
                                                            fg_color = "#53595D",
                                                            button_color = "#53595D",
                                                            corner_radius = 10,
                                                            font = ("Arial", 15),
                                                            dropdown_font = ("Arial", 15),
                                                            dropdown_fg_color = "#727682",)

        #Set all widget comboboxes to "N/A" empty by default and place these using the pack() method
        
        self.Upp_Right_Combo.pack(padx=20, pady=10)
        self.Upp_Right_Combo.set("N/A")

        self.Upp_Left_Combo.pack(padx=20, pady=10)
        self.Upp_Left_Combo.set("N/A")

        self.Centre_Combo.pack(padx=20, pady=10)
        self.Centre_Combo.set("N/A")

        self.BCentre_Combo.pack(padx=20, pady=10)
        self.BCentre_Combo.set("N/A")
        
        #self.wm_attributes("-fullscreen", True)     
        self.geometry("500x500")

        self.Upp_Right_Combo.place(x= 390, y = 90)
        self.Upp_Left_Combo.place(x= 40, y = 90)
        self.Centre_Combo.place(x= 210, y = 350)
        self.BCentre_Combo.place(x= 370, y = 430)



    def Update_List_Widget(self, type):
        RGB = 255 #Set initial RGB value, this will be the text colour of the first element
        for i in range(4): #Use for loop as only 4 items to be displayed due to screen space
            RGB_Hex = (hex(RGB).replace('0x', '')).upper()  #Convert RGB value to hex using hex() method
            RGB_Text_Colour = f"#{RGB_Hex}{RGB_Hex}{RGB_Hex}" #Convert to RGB format for changing text colour
            RGB = RGB - 25 #Decrement hex making it a lighter grey
            if type == "News": #Use selection to process the information accordingly
                    Val = self.Example_News[i].split()
            elif type == "Reminders" or type == "Timetable":
                    Val = self.Tble_RmdInfo[i].split()

    
            Val = " ".join((Val[0:len(Val)//2] + ["\n"] + Val[len(Val)//2::])) #Length too great so a breakline is added

            self.List_Display.text_color = RGB_Text_Colour #Set text colour to RGB value
            self.List_Display.insert(i,Val) #Insert item in location dictated by the for loop

#Widegt screen location methods -----

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
        self.SubmitWidget()

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

        self.SubmitWidget()

        if type  == "Weather":
            self.WeatherWidget(430, 5)

        elif type == "Time/Date":
            self.TimeDate_Widget(380, 20)

        elif type == "Social":
            self.Social_Widget(430, 5) 
        

    def Bott_Centre(self, type): #Used to configure the bottom centre widget in the window
        if type == "N/A": #Check if the widget is to be deleted and if so has it already been created?
            if self.Bott_Centre != "":
                self.Widget_Destroy(self.Bott_Centre_Widget)#If a widget has been created that type "" must be for deletion of the widget
            self.Bott_Centre_Widget = ""
            self.SubmitWidget() #Create submit button widget as a change has occured
            return 

        if self.Bott_Centre_Widget== "":
            #A widget hasnt been created in this location before, therefore "" is for creation of the widget
            self.SubLabel = CTkLabel(master = self, text= "Live as if you were to die tomorrow.", font = ("Arial", 15,), justify = CENTER)
            self.GreetingLabel = CTkLabel(master=self, font = ("Arial", 20, "bold"))
            self.GreetingLabel.place(x = 190, y = 420)
            self.SubLabel.place(x=130, y = 450)
        
        self.Greeting_Widget(type) #Call method to configure widget respective to the type passed in
        self.Bott_Centre_Widget = type #Update Bott_Centre_Widget
        self.SubmitWidget() #Create submit button widget as a change has occured


    def Centre(self,type):
        if type == "N/A":
            if self.Centre_Widget != "":
                self.Widget_Destroy(self.Centre_Widget)
            self.Centre_Widget = ""
            self.SubmitWidget()
            return

        if self.Centre_Widget == "":
            self.List_Display = CTkListbox(self, width = 400, height = 150, border_width= 0,font = ("Arial", 3), justify="centre") #Using CTKListBox class an object is created and stored in the News_Display attribute
            self.List_Display._scrollbar.configure(width = 0) #Editting the objecgs attributes to acheve the desired look
            self.List_Display.place(x = 60, y= 130)
        if type == "Reminders" or type == "Timetable":
            self.Tble_RmdInfo = []
            for i in range(0,4):
                PopUp = CTkInputDialog(text = f"Enter {type} {i}:", title = "Reminders")
                self.Tble_RmdInfo.append(PopUp.get_input())
        self.Update_List_Widget(type)
        self.Centre_Widget = type
        
        self.SubmitWidget()

        
    def WeatherWidget(self,x,y):
            self.WeatherIconWidget = CTkLabel(master = self, text = "", image = self.WeatherIcon)
            self.LocationLabel = CTkLabel(master=self, text= self.Location, font = ("Arial", 15))
            self.TempLabel = CTkLabel(master=self, text= "10°C", font = ("Arial", 15, "bold"))
        
            self.TempLabel.place(x = x-40, y = y+30)
            self.WeatherIconWidget.place(x = x, y = y)
            self.LocationLabel.place(x = x+5, y = y+55)

    def SubmitWidget(self):
        if self.Sub_Butt_Stat == True and self.UppL_Widget == self.UppR_Widget==self.Centre_Widget == self.Bott_Centre_Widget:
            self.SubmitButton.destroy()
            self.Sub_Butt_Stat = False

        elif self.Sub_Butt_Stat == False:
            self.SubmitButton = CTkButton(master = self, text = "Submit", font = ("Arial", 15, "bold"), fg_color="green", command = threading.Thread(target = self.Send_Widget_Data).start)
            self.SubmitButton.place(x = 195, y = 30)
            self.Sub_Butt_Stat = True


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

    def Time_Greeting_Widget(self):
        self.GreetingLabel = CTkLabel(master=self, text= "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!", font = ("Arial", 20, "bold"))
        self.GreetingLabel.place(x = 190, y = 420)

    def Greeting_Widget(self, type):
        if type == "Complement":
            self.GreetingLabel.configure(text = self.Example_Complement)

        elif type == "Time Greet":
            self.GreetingLabel.configure(text = "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!")

        elif type == "Personal Time Greet":
            PopUp = CTkInputDialog(text = "Please enter your name:", title = "Personal Detail")
            self.User_Name = PopUp.get_input()
            self.GreetingLabel.configure(text = ("Good Morning" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon") + " " + self.User_Name)
            self.GreetingLabel.place(x=170,y=420)


    def Social_Widget(self, x, y):

        PopUp = CTkInputDialog(text = "Enter Twitter Username:", title = "Twitter API")
        self.Twitter_Username = PopUp.get_input()

        PopUp = CTkInputDialog(text = "Enter Twitter Password:", title = "Twitter API")
        self.Twitter_Password = PopUp.get_input()

        self.SocialIcon = CTkLabel(master = self, text = "", image = CTkImage(Image.open("Twitter.png"), size = (50,50)))
        self.MessageNotifLabel = CTkLabel(master=self, text= "No messages", font = ("Arial", 15))

        self.MessageNotifLabel.place(x = x-10, y = y+55)
        self.SocialIcon.place(x = x+3, y = y+2)



    def TimeDate_Widget(self, x, y):
        self.TimeLabel = CTkLabel(master=self, text= self.CurrentTime.strftime("%H : %M %p"), font = ("Arial", 25, "bold"))
        self.DateLabel = CTkLabel(master = self, text= f"{self.month} {self.date} {self.Get_Date_Prefix(self.date)}", font = ("Arial", 20, "bold"))

        self.TimeLabel.place(x = x, y = y)
        self.DateLabel.place(x = x, y = y+40)


    def Get_Wifi_Login(self):
        if WifiSelectionWin == None:
            self.WifiSelectionWin = WifiSelection(self)
            self.WifiSelectionWin.focus()
        else:
            self.WifiSelectionWin.focus()
        return


    def Get_Date_Prefix(self,date):
        Prefixes = {1:"st", 2:"nd", 3:"rd"}
        if date % 10 in Prefixes.keys():
                return Prefixes[date%10]
        else:
                return "th"

    def Send_Widget_Data(self):
        global Pi_WifiStatus
        self.SubmitButton.configure(fg_color=("white", "grey"), text = "Updating ...", command = None)
        print(Pi_WifiStatus)
        if Pi_WifiStatus == False:
            with open("Status.txt") as PiStatusFile:
                Pi_Status = PiStatusFile.readlines()
            Pi_WifiStatus = Pi_Status[0].split("=")[1].strip()
            if Pi_WifiStatus == "False":
                WifiInp_Thread = threading.Thread(target = self.Get_Wifi_Login)
                WifiInp_Thread.start()
        else:
                Pi_WifiStatus = True
                Send_Data_Thread = threading.Thread(target = Send_Pi_Data, args=(self.UppL_Widget,self.UppR_Widget,self.Centre_Widget,self.Bott_Centre_Widget,self.User_Name, self.Tble_RmdInfo, self.User_Name))
                Send_Data_Thread.start()
                Send_Data_Thread.join()
                if Data_Sent_Stat == False:
                    CTkMessagebox(title="Connection error", message="Failure to connect, please move device closer and try again", icon="warning")
                else:
                    CTkMessagebox(title="Success", message="Sucess, the mirror will now update", icon="check")
        self.SubmitButton.configure(fg_color=("white", "green"), text = "Submit", command = threading.Thread(target = self.Send_Widget_Data).start)
        return


#Setting up the application envionment
app = App()
#Bluetooth_Thread = threading.Thread(target = app.)
#Bluetooth_Thread.start()
app.mainloop()

