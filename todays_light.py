from datetime import datetime


def todays_light(sunrise_sunset):
   today=datetime.today().strftime('%Y-%m-%d')
    days=sunrise_sunset.get("results")
    for day in days: 
        if day.get("date") == today:
            todayinfo = day
            break
    sunrise=todayinfo.get("sunrise")
    sunset=todayinfo.get("sunset")
    totalminutes=(sunset-sunrise).total_seconds()/60
    
    now=datetime.now()
    relativeminutes=(now-sunrise).total_seconds()/60
    
    