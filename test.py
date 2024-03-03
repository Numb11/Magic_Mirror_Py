def Get_Date_Prefix(date):
        Prefixes = {1:"st", 2:"nd", 3:"rd"}
        if date % 10 in Prefixes.keys():
                return Prefixes[date%10]
        else:
                return "th"

print(Get_Date_Prefix(31))