import requests
response = ("https://api.api-ninjas.com/v1/quotes?category=inspirational")
response = requests.get(response, headers = {"X-Api-Key" : "BmpEwxYiqn0J4zBhTmA91g==OZT1qlY9q3QQJEuN"})
ResponseBody = response.json()
print(ResponseBody[0]["quote"])

#print(ResponseBody["quote"])
#MbaPIfWYyw2eYrdWpi2627211ER9fJnUchpGIj1T	