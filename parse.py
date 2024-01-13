import requests
import json
from datetime import datetime, timezone, timedelta

url = "https://api.dineoncampus.com/v1/location/64b9990ec625af0685fb939d/periods/{0}?platform=0&date={1}"

meals = {"Breakfast":"6595ac33351d530679169c2e","Lunch":"6595ac33351d530679169c21","Dinner":"6595ac33351d530679169c2b"}

days = {}

timezone_offset = -4

days["today"] = datetime.now(timezone(timedelta(hours=timezone_offset))).strftime('%Y-%m-%d')
#days["tomorrow"] = (datetime.today() + timedelta(1)).strftime('%Y-%m-%d')

for day in days:
    header = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Wadsworth Menu</title>
    <link rel="stylesheet" href="style.css">
    <script src="js/meal_handler.js"></script>
  </head>

  <body>
    <div class="meal_selector">
        <h2><a href="#" onclick="breakfast()">Breakfast</a></h2>
        <h2><a href="#" onclick="lunch()">Lunch</a></h2>
        <h2><a href="#" onclick="dinner()">Dinner</a></h2>
    </div>
"""
    body = ""
    for meal in meals:
        data = requests.get(url.format(meals[meal], days[day])).json()

        body = body + f"<div id=\"{meal.lower()}\">\n"
        body = body + f"<div class=\"title\">\n<h1>Wadsworth {meal}</h1>\n<p class=\"sub\">Updated: "
        body = body + str(datetime.now(timezone(timedelta(hours=timezone_offset))).strftime('%a %b %-d at %-I:%M %p\n'))
        body = body + "</p>\n</div>\n<div class=\"tray\">\n"

        empty_stations = ""
        for station in data["menu"]["periods"]["categories"]:
            if len(station["items"]) > 0:
                body = body + "<div class=\"slice\">\n<h2>{0}</h2>\n<hr>\n".format(station["name"])
                for item in station["items"]:
                    body = body + "<h3>{0}</h3>\n".format(item["name"])
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

    with open(f"{day}.html", 'w') as file:
        file.write(header+body+footer)

print(header+body+footer)
