import json
import os
import requests
from flask import Flask, request, make_response, jsonify
from datetime import date

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    req = request.get_json(siltent = True, force = True)
    res = process_webhook(req)
    return jsonify(res)


def process_webhook(req):
    if req["queryResult"]["action"] != "get_weather":
        return {}
    answer = get_weather_data(req)
    return {
        "fulfillmentText": answer,
        "source": "Nomatiom, weatherbit"
    }

def get_city_lat(req):
    searched_city = req["queryResult"]["parameters"]["geo-city"]
    url = "https://nominatim.openstreetmap.org/search/" + str(searched_city) + "?format=json?limit=1"
    coord_data = requests.get(url)
    json_data = coord_data.json()
    lat = json_data[0]["lat"]
    return lat

def get_city_lon(req):
    searched_city = req["queryResult"]["parameters"]["geo-city"]
    url = "https://nominatim.openstreetmap.org/search/" + str(searched_city) + "?format=json?limit=1"
    coord_data = requests.get(url)
    json_data = coord_data.json()
    lon = json_data[0]["lon"]
    return lon

def get_duration(req):
    start_date_raw = req["queryResult"]["parameters"]["date-period"]["startDate"]
    end_date_raw = req["queryResult"]["parameters"]["date-period"]["endDate"]
    start_year = start_date_raw[0:4] 
    end_year = end_date_raw[0:4]
    start_month = start_date_raw[5:7] 
    end_month = end_date_raw[5:7]
    start_day = start_date_raw[8:10]
    end_day = end_date_raw[8:10]
    duration = date(int(end_year), int(end_month), int(end_day)) - date(int(start_year), int(start_month, int(start_day)))
    return duration

def get_weather_data(req):
    searched_city = req["queryResult"]["parameters"]["geo-city"]
    lat = get_city_lat(req)
    lon = get_city_lon(req)
    days = get_duration(req)
    url = "http://api.weatherbit.io/v2.0/forecast/daily?lat=" + str(lat) +  "&lon=" + str(lon) + "&key=5fb6cda4bee1416186784d5ce71a8587&days=" + str(days) 
    weather_data = requests.get(url)
    weather_json = weather_data.json()
    weather = {}
    dates = []
    for step in range(days):
        weather_code = weather_json["data"][step]["weather"]["code"]
        weather_date = weather_json["data"][step]["datetime"]
        weather_temp = weather_json["data"][step]["temp"]
        weather[weather_date] = [weather_code, weather_temp]
        dates.append(weather_date)
        print(weather)
    weather_emojis = {
        1: "⛈",
        2: "🌩",
        3: "💧",
        4: "🌧",
        5: "🌦",
        6: "🌨",
        7: "🌫",
        8: "☀",
        9: "🌤",
        10: "⛅",
        11: "🌥",
        12: "☁"
    }
    stp = 0
    while stp < days:
        print(stp)
        if 200 in weather[dates[stp]] or 201 in weather[dates[stp]] or 202 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[1])
            stp += 1
            print(weather)
            continue
        elif 230 in weather[dates[stp]] or 321 in weather[dates[stp]] or 232 in weather[dates[stp]] or 233 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[2])
            stp += 1
            print(weather)
            continue
        elif 300 in weather[dates[stp]] or 301 in weather[dates[stp]] or 302 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[3])
            stp += 1
            print(weather)
            continue
        elif 500 in weather[dates[stp]] or 501 in weather[dates[stp]] or 502 in weather[dates[stp]] or 511 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[4])
            stp += 1
            print(weather)
            continue
        elif 520 in weather[dates[stp]] or 521 in weather[dates[stp]] or 522 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[5])
            stp += 1
            print(weather)
            continue
        elif 600 in weather[dates[stp]] or 601 in weather[dates[stp]] or 602 in weather[dates[stp]] or 610 in weather[dates[stp]] or 611 in weather[dates[stp]] or 612 in weather[dates[stp]] or 621 in weather[dates[stp]] or 622 in weather[dates[stp]] or 623 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[6])
            stp += 1
            print(weather)
            continue
        elif 700 in weather[dates[stp]] or 711 in weather[dates[stp]] or 721 in weather[dates[stp]] or 731 in weather[dates[stp]] or 741 in weather[dates[stp]] or 751 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[7])
            stp += 1
            print(weather)
            continue
        elif 800 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[8])
            stp += 1
            print(weather)
            continue
        elif 801 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[9])
            stp += 1
            print(weather)
            continue
        elif 802 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[10])
            stp += 1
            print(weather)
            continue
        elif 803 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[11])
            stp += 1
            print(weather)
            continue
        elif 804 in weather[dates[stp]]:
            weather[dates[stp]].append(weather_emojis[12])
            stp += 1
            print(weather)
            continue
    days_list = [x for x in range(days, 0 , -1)]
    dy_weather = []
    for key in weather.keys():
        answr = f"▶📆 {key}: {weather[key][2]}, {weather[key][1]}🌡\n"
        dy_weather.append(answr)
    day_weather = "".join(dy_weather)

    answer = (f"""🔜🌂🌞 Wetterbericht für 📍{searched_city}:
{day_weather}
    """)
    return answer
                


if __Name__ == "main":
    port = int(os.getenv("PORT", 5000))

    print("Starting app on port %d" % port)

app.run(debug=False, port=port, host="0.0.0.0")