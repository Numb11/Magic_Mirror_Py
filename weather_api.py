import requests

response = requests.get("https://gnews.io/api/v4/top-headlines?category=general&max=5&apikey=a0e5514835fad49b0ed972b0c14ec447")
ResponseBody = response.json()
print(ResponseBody)