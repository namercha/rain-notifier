import requests
import os
from twilio.rest import Client

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")  # Twilio account SID
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")  # Twilio auth token
from_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")  # Twilio phone number
to_phone_number = os.environ.get("MY_PHONE_NUMBER")  # Your phone number to get the SMS message.

PARAMS = {
    "lat": 43.073929,
    "lon": -89.385239,  # Madison, WI
    "exclude": "current,minutely,daily",
    "appid": API_KEY,
}

response = requests.get(url=OWM_ENDPOINT, params=PARAMS)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

# print(weather_data["hourly"][1]["weather"]["id"])
# bring_umbrella = False
# for i in range(12):
#     if weather_data["hourly"][i]["weather"][0]["id"] < 700:
#         bring_umbrella = True
# if bring_umbrella:
#     print("Bring an umbrella.")

will_it_rain = False
for hour in weather_slice:
    condition_code = hour["weather"][0]["id"]
    if int(condition_code) < 700:
        will_it_rain = True

if will_it_rain:
    # print("Bring an umbrella.")
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It is going to rain today. Remember to bring an ☔️",
        from_=from_phone_number,
        to=to_phone_number
    )
    print(message.status)
