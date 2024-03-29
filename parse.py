import requests
import json
from datetime import datetime, timezone, timedelta
import sys
import time

headers = {
    'User-Agent': 'Mozilla/5.0'
}

url = "https://api.dineoncampus.com/v1/location/64b9990ec625af0685fb939d/periods/{0}?platform=0&date={1}"

meals = {"Breakfast":"6595ac33351d530679169c2e","Lunch":"6595ac33351d530679169c21","Dinner":"6595ac33351d530679169c2b"}

days = {}

timezone_offset = -4

days["Today"] = datetime.now(timezone(timedelta(hours=timezone_offset))).strftime('%Y-%m-%d')
days["Tomorrow"] = (datetime.now(timezone(timedelta(hours=timezone_offset))) + timedelta(1)).strftime('%Y-%m-%d')

print(days)


for day in days:
    header = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Wadsworth Menu</title>
    <link rel="stylesheet" href="style.css">
    <script src="js/meal_handler.js"></script>
  </head>

  <body>"""

    meal_selector = """
    <div class=\"meal_selector\">
      <h2 class="days" id="today"><a href="today.html"><span>&lt;</span> Prev</a></hr>
      <h2><a href=\"#\" onclick=\"breakfast()\">Breakfast</a></h2>
      <h2><a href=\"#\" onclick=\"lunch()\">Lunch</a></h2>
      <h2><a href=\"#\" onclick=\"dinner()\">Dinner</a></h2>
      <h2 class="days" id="tomorrow"><a href="tomorrow.html">Next<span>&gt;</span></a></hr>
    </div>"""

    body = header + meal_selector

    for meal in meals:
        time.sleep(3)
        request = requests.get(url.format(meals[meal], days[day]), headers=headers)
        request.raise_for_status()
        if request.status_code != 204:
            data = request.json()
        else:
            print("It's probably time to use selenium...")
            sys.exit()

        body = body + f"<div id=\"{meal.lower()}\">\n"
        body = body + f"<div class=\"title\">\n<h1>Wadsworth {meal} {day}</h1>\n<p class=\"sub\">Updated: "
        body = body + str(datetime.now(timezone(timedelta(hours=timezone_offset))).strftime('%a %b %-d at %-I:%M %p\n'))
        body = body + "</p>\n</div>\n<div class=\"tray\">\n"
        
        empty_stations = ""
        for station in data["menu"]["periods"]["categories"]:
            if len(station["items"]) > 0:
                body = body + "<div class=\"slice\">\n<h2>{0}</h2>\n<hr>\n".format(station["name"])
                for item in station["items"]:
                    body = body + "<p>{0}</p>\n".format(item["name"])
                    if item["desc"]:
                        body = body + "<p class=\"smol\">{0}</p>\n".format(item["desc"])
                    else:
                        body = body + "<br>\n"
                body = body + "</div>\n"
            else:
                empty_stations = empty_stations + "<div class=\"slice\">\n<h2>{0}</h2>\n<hr>\n</div>\n".format(station["name"])

        body = body + empty_stations
        body = body + "</div>\n</div>\n"

    footer = "</body></html>"

    lower_day = day.lower()

    with open(f"{lower_day}.html", 'w') as file:
        file.write(header+body+footer)


print(header+body+footer)
