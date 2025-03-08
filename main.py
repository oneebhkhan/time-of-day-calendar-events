
import fire
import pytz
import requests
from ics import Calendar, Event
from datetime import timedelta, datetime


def get_lat_lon(location):
    request = requests.get(f"https://geocode.xyz/{location}?json=1")

    if request.status_code == 200:
        data = request.json()
        lat = data["latt"]
        lon = data["longt"]

        return lat, lon
    else:
        raise Exception("Failed to get lat/lon")


def get_prayer_times(date, lat, lon):
    request = requests.get(f"http://api.aladhan.com/v1/timings/{date}?latitude={lat}&longitude={lon}")

    if request.status_code == 200:

        data = request.json()
        time_zone = pytz.timezone(data["data"]["meta"]["timezone"])
        sehri_timing = data["data"]["timings"]["Fajr"]
        iftar_timing = data["data"]["timings"]["Maghrib"]

        return sehri_timing, iftar_timing, time_zone
    else:
        raise Exception("Failed to get prayer times")


# create a calendar event
def create_event(start_time, duration, name, location):
    event = Event()
    event.name = name
    event.begin = start_time
    event.duration = duration
    event.location = location

    return event


# save events to calendar
def create_calendar(start_date, num_days, duration, location, fiqh='Hanafi', adjustment=0):

    lat, lon = get_lat_lon(location)
    if fiqh == 'Jafari' and adjustment == 0:
        adjustment = 10
    elif fiqh == 'Hanafi':
        adjustment = 0

    events = []

    for i in range(num_days):
        date = (datetime.strptime(start_date, "%d-%m-%Y") + (i * timedelta(days=1))).strftime("%d-%m-%Y")
        suhoor_time, iftar_time, time_zone = get_prayer_times(date, lat, lon)

        converted_date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        suhoor_time_dt = time_zone.localize(datetime.strptime(f"{converted_date} {suhoor_time}", "%Y-%m-%d %H:%M") - timedelta(minutes=adjustment))
        iftar_time_dt = time_zone.localize(datetime.strptime(f"{converted_date} {iftar_time}", "%Y-%m-%d %H:%M") + timedelta(minutes=adjustment))

        suhoor_event = create_event(suhoor_time_dt, timedelta(minutes=duration), f"🌅Suhoor@{location}  ", location)
        iftar_event = create_event(iftar_time_dt, timedelta(minutes=duration), f"🌇 Iftar@{location}", location)

        events.append(suhoor_event)
        events.append(iftar_event)

    cal = Calendar()
    cal.events = events

    # save the calendar to a file
    with open(f"Ramzan@{location}-{fiqh}.ics", "w") as f:
        f.writelines(cal)


fire.Fire(create_calendar)
