import json
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
    

def get_city_lat(req):
    searched_city = req["queryResult"]["parameters"]["geo-city"]
    url = "https://nominatim.openstreetmap.org/search/" + str(searched_city) + "?format=json?limit=1"
    coord_data = request.get(url)
    json_data = coord_data.json()
    lat = json_data[0]["lat"]
    return lat

def get_city_lon(req):
    searched_city = req["queryResult"]["parameters"]["geo-city"]
    url = "https://nominatim.openstreetmap.org/search/" + str(searched_city) + "?format=json?limit=1"
    coord_data = request.get(url)
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
    lat = get_city_lat(req)
    lon = get_city_lon(req)
    days = get_duration(req)
    url = "http://api.weatherbit.io/v2.0/forecast/daily?lat=" + str(lat) +  "&lon=" + str(lon) + "&key=5fb6cda4bee1416186784d5ce71a8587&days=" + str(days) 
    weather_data = request.get(url)
    weather_json = weather_data.json()
    weather = {}
    for step in range(days):
        weather_code = weather_json["data"][step]["weather"]["code"]
        weather_date = weather_json["data"][step]["datetime"]
        weather_temp = weather_json["data"][step]["temp"]
        weather[weather_date] = [weather_code, weather_temp]
        print(weather)
    return weather
