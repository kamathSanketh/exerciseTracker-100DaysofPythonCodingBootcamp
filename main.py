import requests
from datetime import datetime
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
url = os.environ["nutritionix_endpoint"]
sheety_url = os.environ["sheety_endpoint"]
user_input = input("Enter your exercise: ")
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
params = {
    "query": user_input,
    "gender": "male",
    "weight_kg": "72.5",
    "height_cm": "167.64",
    "age": "30"
}
response = requests.post(url, json=params, headers=headers)
response.raise_for_status()
result = response.json()
bearer = os.environ["bearer"]
sheety_headers = {"Authorization": bearer}
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
for x in result["exercises"]:
    sheety_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": x["name"].title(),
            "duration": x["duration_min"],
            "calories": x["nf_calories"]
        }
    }
    sheety_response = requests.post(sheety_url, json=sheety_inputs, headers=sheety_headers)
    print(sheety_response.text)
