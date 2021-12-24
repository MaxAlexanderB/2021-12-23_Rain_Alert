import requests
from twilio.rest import Client
import os

#---------Optionally set up python anywhere---------#
#---------Set variables and call environmental variables-------#
OWM_endpoint = "http://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ['api_key']
account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
twilio_number = os.environ['twilio_number']
my_phone = os.environ['my_phone']

#----------Set params for API, problem api_key is in URL which isn't safe---------#
parameters = {
    "lat":46.947975,
    "lon":7.447447,
    "appid":api_key,
    "exclude": 'current,minutely,daily'
}

#----------Get json--------#
response = requests.get(OWM_endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()


#---------Select data from json--------#
next_12_hours = {hour+1: weather_data['hourly'][hour]['weather'][0]['id'] for hour in range(0,12)}
print(next_12_hours)

#--------Set loop for when it will rain------#
will_rain = False

for hour, code in next_12_hours.items():
    if code < 700:
        will_rain = True

if will_rain:
    #--------create client object from the twilio client class--------#
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It will rain",
        from_=twilio_number,
        to=my_phone
    )
    #-------check status------@
    print(message.status)
