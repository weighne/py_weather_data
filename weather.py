import requests  # for getting the data from the web


def deg_to_cardinal(deg):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(deg / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


def get_wind(wind_data):
    dir = deg_to_cardinal(int(wind_data[0:3]))
    speed = wind_data[3:5]

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
			temp = x.split("/")[0]
			dewpoint = x.split("/")[1]
		except IndexError:
			temp = x
	elif "KT" in x:
		wind_dir, wind_speed = get_wind(x)

print(weather)

print(f"Temp: {temp}\nDewpoint: {dewpoint}\nWindDir: {wind_dir}\nWindSpeed: {wind_speed}")
