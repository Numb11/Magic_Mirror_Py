#Windows Side
import datetime
import socket
import customtkinter
from CTkListbox import *
from CTkMessagebox import *
from customtkinter import *
from PIL import Image
from tkinter import mainloop
import threading


PIMACAddress = "00:1f:e1:dd:08:3d"
PORT = 5
def Send_Pi_Data(UL,UR,BCENT,CENT):
    try:
        BlueSock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        for i in range(3):
            if BlueSock.connect((PIMACAddress, PORT)) == 0:
                BlueSock.send(bytes(UL,UR,BCENT,CENT, "UTF-8"))
                BlueSock.close()
                return True
        BlueSock.close()
        return False
    except:
        return False


class App(customtkinter.CTk): #Class that is used for the main applicaiton window

    def __init__(self, *args, **kwargs): #Non-keyword and keyword arguments can be passed in, packed as dictionary
        super().__init__(*args, **kwargs) #Expand non-keyword and keyword dictionary into arguments 

        self.Example_News = ["More lives lost than saved in Troubles due to British spy, report finds",
                                "Justin Welby says he carries personal alarm amid increasing threats in church",
                                "Head of UK science body calls for ‘creative disagreement’ after Michelle Donelan libel row",
                                "BP claws back £1.8m from sacked boss Looney and hands new CEO £8m pay deal"]
        
        self.Example_Reminders = ["Take the Dog for a walk",
                                "Jane's Birthday party - 3pm",
                                "Get shopping",
                                "Mow the grass"]
        
        self.Example_Timetable = ["09:00 - COMCORE1C Lecture",
                                "10:00 - COMCORE2C Lecture",
                                "13:00 - Dinner",
                                "14:35 - COMCORE1C Lecture"]

        self.Example_Complement = "You look nice!"
        self.Location = "Location"
        self.UppR_Widget = ""
        self.UppL_Widget = ""
        self.Centre_Widget = ""
        self.Bott_Centre_Widget = ""
        self.Sub_Butt_Stat = False

        #Weather data and graphic ---------------
        self.WeatherIcon = CTkImage(Image.open("01d@2x.png"), size = (70,70)) #Store CTKimage object with argument as Image.open() method result store this in the WeatherIocn attribute
        

        #Time handling, storing of essential time and date informaiton ----------
        self.CurrentTime = datetime.datetime.now() 
        self.month = self.CurrentTime.strftime("%B")
        self.date = int(self.CurrentTime.strftime("%d"))



        self.Upp_Right_Combo = CTkOptionMenu(master = self,
                                                            values =["Weather", "Time/Date", "Social", "N/A"],
                                                            command = self.Upp_Right,
                                                            width = 35,
                                                            fg_color = "#53595D",
                                                            button_color = "#53595D",
                                                            corner_radius = 10,
                                                            font = ("Modern No. 20", 15),
                                                            dropdown_font = ("Modern No. 20", 15),
                                                            dropdown_fg_color = "#727682",)
        
        self.Upp_Left_Combo = CTkOptionMenu(master = self,
                                                            values =["Weather", "Time/Date", "Social", "N/A"],
                                                            command = self.Upp_Left,
                                                            width = 35,
                                                            fg_color = "#53595D",
                                                            button_color = "#53595D",
                                                            corner_radius = 10,
                                                            font = ("Modern No. 20", 15),
                                                            dropdown_font = ("Modern No. 20", 15),
                                                            dropdown_fg_color = "#727682",)
        
        self.Centre_Combo = CTkOptionMenu(master = self,
                                                            values =["News", "Reminders", "Timetable", "N/A"],
                                                            command = self.Centre,
                                                            width = 35,
                                                            fg_color = "#53595D",
                                                            button_color = "#53595D",
                                                            corner_radius = 10,
                                                            font = ("Modern No. 20", 15),
                                                            dropdown_font = ("Modern No. 20", 15),
                                                            dropdown_fg_color = "#727682",)
        

        self.BCentre_Combo = CTkOptionMenu(master = self,
                                                            values =["Complement", "Time Greet", "Personal Time Greet","N/A"],
                                                            command = self.Bott_Centre,
                                                            width = 35,
                                                            fg_color = "#53595D",
                                                            button_color = "#53595D",
                                                            corner_radius = 10,
                                                            font = ("Modern No. 20", 15),
                                                            dropdown_font = ("Modern No. 20", 15),
                                                            dropdown_fg_color = "#727682",)


        
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
        RGB = 192
        for i in range(4):
            RGB_Hex = (hex(RGB).replace('0x', '')).upper()
            RGB_Text_Colour = f"#{RGB_Hex}{RGB_Hex}{RGB_Hex}"
            RGB = RGB - 25
            
            if type == "News":
                    Val = self.Example_News[i].split()
            elif type == "Reminders":
                    Val = self.Example_Reminders[i].split()
            elif type == "Timetable":
                    Val = self.Example_Timetable[i].split()

            Val = " ".join((Val[0:len(Val)//2] + ["\n"] + Val[len(Val)//2::]))
            self.List_Display.text_color = RGB_Text_Colour
            self.List_Display.insert(i,Val)
            self.List_Display.text_color = "Default"


    def Upp_Left(self,type):

        if type == self.UppR_Widget:
            self.Widget_Destroy(self.UppR_Widget)
            self.UppR_Widget = ""

        self.Widget_Destroy(self.UppL_Widget)
        if type == "N/A":
            self.UppL_Widget = ""
        else:
            self.UppL_Widget = type  
        
        self.SubmitWidget()

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

        self.SubmitWidget()

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
            self.SubmitWidget()
            return 

        if self.Bott_Centre_Widget== "":
            self.SubLabel = CTkLabel(master = self, text= "Live as if you were to die tomorrow.", font = ("Modern No. 20", 15,), justify = CENTER)
            self.GreetingLabel = CTkLabel(master=self, font = ("Modern No. 20", 20, "bold"))
            self.GreetingLabel.place(x = 190, y = 420)
            self.SubLabel.place(x=130, y = 450)
        
        self.Greeting_Widget(type)
        self.Bott_Centre_Widget = type
        self.SubmitWidget()


    def Centre(self,type):
        if type == "N/A":
            if self.Centre_Widget != "":
                self.Widget_Destroy(self.Centre_Widget)
            self.Centre_Widget = ""
            self.SubmitWidget()
            return

        if self.Centre_Widget == "":
            self.List_Display = CTkListbox(self, width = 400, height = 150, border_width= 0,font = ("Modern No. 20", 3), justify="centre") #Using CTKListBox class an object is created and stored in the News_Display attribute
            self.List_Display._scrollbar.configure(width = 0) #Editting the objecgs attributes to acheve the desired look
            self.List_Display.place(x = 60, y= 130)

        self.Update_List_Widget(type)
        self.Centre_Widget = type
        
        self.SubmitWidget()

        
    def WeatherWidget(self,x,y):
            self.WeatherIconWidget = CTkLabel(master = self, text = "", image = self.WeatherIcon)
            self.LocationLabel = CTkLabel(master=self, text= self.Location, font = ("Modern No. 20", 15))
            self.TempLabel = CTkLabel(master=self, text= "10°C", font = ("Modern No. 20", 15, "bold"))
        
            self.TempLabel.place(x = x-40, y = y+30)
            self.WeatherIconWidget.place(x = x, y = y)
            self.LocationLabel.place(x = x+5, y = y+55)

    def SubmitWidget(self):
        if self.Sub_Butt_Stat == True and self.UppL_Widget == self.UppR_Widget==self.Centre_Widget == self.Bott_Centre_Widget:
            self.SubmitButton.destroy()
            self.Sub_Butt_Stat = False

        elif self.Sub_Butt_Stat == False:
            self.SubmitButton = CTkButton(master = self, text = "Submit", font = ("Modern No. 20", 15, "bold"), fg_color="green", command = threading.Thread(target = self.Send_Widget_Data).start)
            self.SubmitButton.place(x = 195, y = 30)
            self.Sub_Butt_Stat = True


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

        elif type == "Complement":
            self.GreetingLabel.destroy()
            self.SubLabel.destroy()
        
        elif type in ["News", "Reminders", "Timetable"]:
            self.List_Display.destroy()

    def Time_Greeting_Widget(self):
        self.GreetingLabel = CTkLabel(master=self, text= "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!", font = ("Modern No. 20", 20, "bold"))
        self.GreetingLabel.place(x = 190, y = 420)

    def Greeting_Widget(self, type):
        if type == "Complement":
            self.GreetingLabel.configure(text = self.Example_Complement)

        elif type == "Time Greet":
            self.GreetingLabel.configure(text = "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!")

        elif type == "Personal Time Greet":
            PopUp = CTkInputDialog(text = "Please enter your name:", title = "Personal Detail")
            self.User_Name = PopUp.get_input()
            self.GreetingLabel.configure(text = "Good Morning" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon" + " " + self.User_Name + "!")
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
        self.DateLabel = CTkLabel(master = self, text= f"{self.month} {self.date} {self.Get_Date_Prefix(self.date)}", font = ("Modern No. 20", 20, "bold"))

        self.TimeLabel.place(x = x, y = y)
        self.DateLabel.place(x = x, y = y+40)

    def Quote_Widget(self):
        self.QuoteLabel.configure()


    def Get_Date_Prefix(self,date):
        Prefixes = {1:"st", 2:"nd", 3:"rd"}
        if date % 10 in Prefixes.keys():
                return Prefixes[date%10]
        else:
                return "th"

    def Send_Widget_Data(self):

        self.SubmitButton.configure(fg_color=("white", "grey"), text = "Updating ...", command = None)

        Data_To_Send = {"UL": self.UppL_Widget,
                        "UR": self.UppR_Widget,
                        "Cent": self.Centre_Widget,
                        "BCent": self.Bott_Centre_Widget}
        
        Send_Data_Thread = threading.Thread(target = Send_Pi_Data, args=(Data_To_Send))
        Send_Data_Thread.start()
        if Send_Data_Thread.join()== False:
            CTkMessagebox(title="Connection error", message="Failure to connect, please move device closer andtry again", icon="warning")
        else:
            CTkMessagebox(title="Success", message="Sucess, the mirror should have updated", icon="check")

        self.SubmitButton.configure(fg_color=("white", "green"), text = "Submit", command = threading.Thread(target = self.Send_Widget_Data).start)

        return


#Setting up the application envionment
app = App()
#Bluetooth_Thread = threading.Thread(target = app.)
#Bluetooth_Thread.start()
app.mainloop()

