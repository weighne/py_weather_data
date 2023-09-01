import requests  # for getting the data from the web
import re


def deg_to_cardinal(deg):  # stolen from https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(deg / (360. / len(dirs)))

    return dirs[ix % len(dirs)]


def clouds(cloud_data):
    clouds = ""
    cloud_types = {"CLR":"Clear",
                   "FEW":"Mostly Sunny",
                   "SCT":"Partly Cloudy",
                   "BKN":"Mostly Cloudy",
                   "OVC":"Cloudy"}
    for key, value in cloud_types.items():
        if key == cloud_data[:3]:
            clouds = value
        else: continue

    return clouds


def get_wind(wind_data):
    gusts = "N/A"

    if wind_data[0:3].isalpha():
        dir = wind_data[0:3]
    else:
        dir = deg_to_cardinal(int(wind_data[0:3]))

    if "G" in wind_data:
        speed = int(wind_data[3:5]) * 1.852
        gusts = int(wind_data[6:8]) * 1.852
    else:
        speed = int(wind_data[3:].strip("KT")) * 1.852

    return dir, str(speed)+" km/h", str(gusts)+" km/h"


def get_atmo_pres(atmo_data):
    pressure = atmo_data.strip("A")
    millibar = int(pressure) * 338639 / 1000000

    return str(round(millibar, 2)) + " millibars"


if __name__ == '__main__':
    station = input("Enter weather station: ").upper().strip()
    url = f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{station}.TXT"

    weather_data = requests.get(url)

    lines = [line for line in weather_data.text.splitlines()]

    weather = lines[1].split(" ")

    formatted_data = {"Temp":"",
                      "Dewpoint":"",
                      "WindDir":"",
                      "WindSpeed":"",
                      "WindGusts":"",
                      "Sky":"",
                      "AtmosphericPressure":""}

    for x in weather:
        if "/" in x:  # temp and dewpoint
            try:
                formatted_data["Temp"] = x.split("/")[0].replace("M","-") + " C"
                formatted_data["Dewpoint"] = x.split("/")[1].replace("M","-") + " C"
            except IndexError:
                formatted_data["Temp"] = x
        elif "KT" in x:  # wind
            formatted_data["WindDir"], formatted_data["WindSpeed"], formatted_data["WindGusts"] = get_wind(x)
        elif "FEW" in x or "SCT" in x or "BKN" in x or "OVC" in x or "CLR" in x:  # clouds
            formatted_data["Sky"] = clouds(x)
        elif "A" in x and re.match("A[0-9]+",x):
            formatted_data["AtmosphericPressure"] = get_atmo_pres(x)
            # print(x)

    for x, y in formatted_data.items():
        if "N/A" in y or y == "": continue
        else:
            print(f"{x}: {y}")
