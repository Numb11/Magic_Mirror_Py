#Windows Side
import datetime
import threading
import customtkinter
from CTkListbox import *
from customtkinter import *
from PIL import Image
from tkinter import mainloop
import time

'''class Pop_Up_Win(customtkinter.CTk):
    def __init__(self,Pop_Up_Type,App *args, **kwargs): #Non-keyword and keyword arguments can be passed in, packed as dictionary
        super().__init__(*args, **kwargs) #Expand non-keyword and keyword dictionary into arguments 
        self.Pop_Up_Type = Pop_Up_Type

        self.Username, self.Password = ""
        self.InputButton = CTkInputDialog(self, text ="Submit", command = self.Submit_Button)
        self.Username_TextB = CTkTextbox(self, text = "Username:")
        self.Password_TextB = CTkTextbox(self, text = "Password:")
        self.Input_TextB = CTkTextbox(self)



    def Display_Pop_Up(self):
        if self.Pop_Up_Type == "Auth":
            self.Username_TextB.place(x = 20, y= 10)
            self.Password_TextB.place(x = 20, y= 20)

        else:
            self.Input_TextB(x = 20, y= 10)
        
        self.InputButton.place(x = 20, y= 30)

    def Submit_Button(self):
        self.Username = self.Username_TextB.get_input()
        self.Password = self.Password_TextB.get_input()
        self.GenInput = self.Input_TextB.get_input()


    def Get_Input(self):
        return {"Username": self.Username,"Password": self.Password, "Input" : self.GenInput}

    def Close_PopUp(self):
        self.destroy() '''

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

        self.Example_Complement = "You look nice!"
        self.Location = "Location"
        self.UppR_Widget = ""
        #Weather data and graphic ---------------
        self.WeatherIcon = CTkImage(Image.open("01d@2x.png"), size = (70,70)) #Store CTKimage object with argument as Image.open() method result store this in the WeatherIocn attribute
        
        #News data and grpahic -----------------
        self.List_Display = CTkListbox(self, width = 400, height = 500, border_width= 0,font = ("Modern No. 20", 3), justify="centre") #Using CTKListBox class an object is created and stored in the News_Display attribute
        self.List_Display._scrollbar.configure(width = 0) #Editting the objecgs attributes to acheve the desired look

        #Time handling, storing of essential time and date informaiton ----------
        self.CurrentTime = datetime.datetime.now() 
        self.month = self.CurrentTime.strftime("%B")
        self.date = int(self.CurrentTime.strftime("%d"))



        self.Upp_Right_Combo = CTkOptionMenu(master = self,
                                                            values =["Weather", "Time/Date", "Social"],
                                                            command = self.Upp_Right,
                                                            width = 35,
                                                            fg_color = "#727682",
                                                            button_color = "#42454c",
                                                            corner_radius = 10,)
        
        self.Upp_Right_Combo.pack(padx=20, pady=10)
        self.Upp_Right_Combo.set("Weather")


        
        #self.wm_attributes("-fullscreen", True)     
        self.geometry("500x500")

        #Defininf widget objects of CustomTkinter and storing in unique attributes
        '''self.WeatherIconWidget = CTkLabel(master = self, text = "", image = self.WeatherIcon)
        self.LocationLabel = CTkLabel(master=self, text= self.Location, font = ("Modern No. 20", 15))
        self.TempLabel = CTkLabel(master=self, text= "10°C", font = ("Modern No. 20", 15, "bold"))
        self.TimeLabel = CTkLabel(master=self, text= self.CurrentTime.strftime("%H : %M %p"), font = ("Modern No. 20", 25, "bold"))
        self.DateLabel = CTkLabel(master = self, text= f"{self.month} {self.date} {self.Get_Date_Prefix(self.date)}", font = ("Modern No. 20", 20, "bold"))
        self.QuoteLabel = CTkLabel(master = self, text= "Live as if you were to die tomorrow.", font = ("Modern No. 20", 15,), justify = CENTER)
        self.GreetingLabel = CTkLabel(master=self, text= "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!", font = ("Modern No. 20", 20, "bold"))

        #Choosing the locaiton of elmen ts defined above
        self.List_Display.place(x = 60, y= 130)
        self.TempLabel.place(x = 390, y = 35)
        self.WeatherIconWidget.place(x = 430, y = 5)
        self.LocationLabel.place(x = 435, y = 60)
        self.GreetingLabel.place(x = 190, y = 420)
        self.TimeLabel.place(x = 20, y = 20)
        self.DateLabel.place(x = 20, y = 60)
        self.QuoteLabel.place(x=130, y = 450)'''

        self.Upp_Right_Combo.place(x= 390, y = 90)

    def Update_List_Widget(self, type):
        print("test")
        RGB = 192
        for i in range(4):
            RGB_Hex = (hex(RGB).replace('0x', '')).upper()
            RGB_Text_Colour = f"#{RGB_Hex}{RGB_Hex}{RGB_Hex}"
            RGB = RGB - 25
            
            if type == "News":
                    Val = self.Example_News.split()
            else:
                    Val = self.Example_Reminders.split()

            if len(Val) > 4 and len(self.Example_News[i]) > 20:
                Val = " ".join((Val[0:len(Val)//2] + ["\n"] + Val[len(Val)//2::]))
                self.List_Display.text_color = RGB_Text_Colour
                self.List_Display.insert(i,Val)
                self.List_Display.text_color = "Default"




    def WeatherWidget(self,x,y):
            self.WeatherIconWidget = CTkLabel(master = self, text = "", image = self.WeatherIcon)
            self.LocationLabel = CTkLabel(master=self, text= self.Location, font = ("Modern No. 20", 15))
            self.TempLabel = CTkLabel(master=self, text= "10°C", font = ("Modern No. 20", 15, "bold"))
        
            self.TempLabel.place(x = x-40, y = y+30)
            self.WeatherIconWidget.place(x = x, y = y)
            self.LocationLabel.place(x = x+5, y = y+55)



    def Widget_Destroy(self, type):
        if type == "Weather" :
            self.TempLabel.destroy()
            self.WeatherIconWidget.destroy()
            self.LocationLabel.destroy()
            
        if type == "Time/Date":
            self.TimeLabel.destroy()
            self.DateLabel.destroy()

        if type == "Social":
            self.MessageNotifLabel.destroy()
            self.SocialIcon.destroy()


    def Upp_Right(self,type):
        self.Widget_Destroy(self.UppR_Widget)
        self.UppR_Widget = type
        if type  == "Weather":
            self.WeatherWidget(430, 5)

        elif type == "Time/Date":
            self.TimeDate_Widget(380, 20)

        elif type == "Social":
            self.Social_Widget(430, 5)
            

    def Time_Greeting_Widget(self):
        self.GreetingLabel = CTkLabel(master=self, text= "Good Morning!" if int(self.CurrentTime.strftime("%H"))<12 else "Good Afternoon!", font = ("Modern No. 20", 20, "bold"))
        self.GreetingLabel.place(x = 190, y = 420)

    def Complement_Greeting_Widget(self):
        self.GreetingLabel.configure(self.Example_Complement)

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




#Setting up the application envionment
app = App()
#Bluetooth_Thread = threading.Thread(target = app.)
#Bluetooth_Thread.start()
app.mainloop()

