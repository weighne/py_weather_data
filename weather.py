import requests  # for getting the data from the web


def deg_to_cardinal(deg):  # stolen from https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(deg / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


def clouds(cloud_data):
    cloud_types = {"FEW":"Mostly Sunny",
                   "SCT":"Partly Cloudy",
                   "BKN":"Mostly Cloudy",
                   "OVC":"Cloudy"}
    for key, value in cloud_types.items():
        if key == cloud_data[:3]:
            return value
        else: continue

def get_wind(wind_data):
    dir = deg_to_cardinal(int(wind_data[0:3]))
    speed = wind_data[3:]

    return dir, speed


url = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/KMGJ.TXT"

weather_data = requests.get(url)

# print(weather_data.text)

lines = [line for line in weather_data.text.splitlines()]

timestamp = lines[0]
weather = lines[1].split(" ")
temp = ""
dewpoint = ""
sky_cover = ""
wind_speed = ""
gust_speed = ""
wind_dir = ""
atmo_pres = ""


for x in weather:
	if "/" in x:  # temp and dewpoint
		try:
			temp = x.split("/")[0].replace("M","-")
			dewpoint = x.split("/")[1].replace("M","-")
		except IndexError:
			temp = x
	elif "KT" in x:
		wind_dir, wind_speed = get_wind(x)
	elif "FEW" in x or "SCT" in x or "BKN" in x or "OVC" in x:
	    sky_cover = clouds(x)

print(weather)

print(f"Temp: {temp}\nDewpoint: {dewpoint}\nWindDir: {wind_dir}\nWindSpeed: {wind_speed}\nSky: {sky_cover}")
