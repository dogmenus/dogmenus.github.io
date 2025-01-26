import requests
import json
from datetime import datetime, timezone, timedelta
import sys
import time

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0'
}

period_url = "https://api.dineoncampus.com/v1/location/{0}/periods?platform=0&date={1}"

food_url = "https://api.dineoncampus.com/v1/location/{0}/periods/{1}?platform=0&date={2}"

halls = {"Wadsworth":"64b9990ec625af0685fb939d","McNair":"64a6b628351d5305dde2bc08","DHH":"64e3da15e45d430b80c9b981"}

days = {}

timezone_offset = -4

days["Today"] = datetime.now(timezone(timedelta(hours=timezone_offset))).strftime('%Y-%m-%d')
days["Tomorrow"] = (datetime.now(timezone(timedelta(hours=timezone_offset))) + timedelta(1)).strftime('%Y-%m-%d')

header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Wadsworth Menu</title>
    <link rel="stylesheet" href="../style.css">
    <script src="../js/meal_handler.js"></script>
</head>

<body>"""

meal_selector = """
    <div class=\"meal_selector\">
    <h2 class="days" id="today"><a href="today.html"><span>&lt;</span> Prev</a></h2>
    <h2><a href=\"#\" onclick=\"breakfast()\">Breakfast</a></h2>
    <h2><a href=\"#\" onclick=\"lunch()\">Lunch</a></h2>
    <h2><a href=\"#\" onclick=\"dinner()\">Dinner</a></h2>
    <h2 class="days" id="tomorrow"><a href="tomorrow.html">Next<span>&gt;</span></a></h2>
    </div>"""

footer = """<div class=\"title\">
    <h2 style=\"font-size:12pt;\"><a href=\"../index.html\">About This Project</a></h2>
</div>
<a class=\"home\" href=\"../index.html\">Home</a>
</body></html>"""


for hall in halls:
    for day in days:

        url_string = period_url.format(halls[hall], days[day])
        print(f"Fetching periods from {url_string}")
        request = requests.get(url_string, headers=headers, timeout=20)
        time.sleep(6)
        request.raise_for_status()
        if request.status_code != 204:
            data = request.json()
        else:
            print("It's probably time to use selenium...")
            sys.exit()

        #print(data)

        meals = {"Breakfast":"closed","Lunch":"closed","Dinner":"closed"}

        if not data["closed"]:
            for period in data["periods"]:
                match period["name"]:
                    case "Breakfast":
                        meals["Breakfast"] = period["id"]
                    case "Lunch":
                        meals["Lunch"] = period["id"]
                    case "Dinner":
                        meals["Dinner"] = period["id"]

        body = meal_selector
        
        for meal in meals:
            body = body + f"<div id=\"{meal.lower()}\">\n"
            body = body + f"<div class=\"title\">\n<h1>{hall} {meal} {day}</h1>\n<p class=\"sub\">Updated: "
            body = body + str(datetime.now(timezone(timedelta(hours=timezone_offset))).strftime('%a %b %-d at %-I:%M %p\n'))+ "</p>\n"

            if data["closed"] or meals[meal] == "closed":
                    body = body + "<br><h2>It doesn't look like this hall is open for this meal...</h2><br><br>"
            else:
                url_string = food_url.format(halls[hall], meals[meal], days[day])
                print(f"Fetching {url_string}")
                request = requests.get(url_string, headers=headers, timeout=20)
                time.sleep(6)
                request.raise_for_status()
                if request.status_code != 204:
                    data = request.json()
                else:
                    print("It's probably time to use selenium...")
                    sys.exit()

                #print(data);

                body = body + "</div>\n<div class=\"tray\">\n"
                
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
        

        lower_day = day.lower()
        lower_hall= hall.lower()

        with open(f"{lower_hall}/{lower_day}.html", 'w') as file:
            file.write(header+body+footer)
            print(f"Completed {hall} {lower_day}!")
