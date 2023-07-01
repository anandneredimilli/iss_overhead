'''track iss latitude and longitude if it matches (that match should be in n8) with our location coordinates we will be notified'''

import requests
import datetime
import pytz #used to convert the timezones
import ssl
import smtplib
from email.message import EmailMessage

email_sender = "anandn9804@gmail.com"
email_password = "ptoyfxljjsjylsgl"
email_receiver = email_sender
MY_LAT = 16.518901
MY_LONG = 81.361897




def is_iss_overhead():
    iss_position = requests.get('http://api.open-notify.org/iss-now.json').json()
    iss_lattitude = float(iss_position['iss_position']['latitude'])
    iss_longitude = float(iss_position['iss_position']['longitude'])

    if MY_LAT-5<iss_lattitude<MY_LAT+5 and MY_LONG-5<iss_longitude<MY_LONG+5:
        return True
     
def is_night():
    coordinates_dict = {
    'lat':MY_LAT,
    'lng':MY_LONG,
    'formatted':0
}

    data = requests.get('https://api.sunrise-sunset.org/json',params=coordinates_dict).json() 
    sunrise_time = int(data['results']['sunrise'].split('T')[1].split(':')[0]) #extracting the hour of sunrise and sunset, to understand break the expression and use print
    sunset_time = int(data['results']['sunset'].split('T')[1].split(':')[0])
    #get local ist time in utc format
    time_now_in_utc = datetime.datetime.now(pytz.utc).hour
    if time_now_in_utc <= sunrise_time or time_now_in_utc >= sunset_time:
        #print("night")
        return True

if is_iss_overhead and is_night:
    message = ' iss is moving over you'
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = "Test Subject"
    em.set_content(message)

    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls(context=context)
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

#host this code online and make it run for every minute, so that if iss passes above us i will get an email