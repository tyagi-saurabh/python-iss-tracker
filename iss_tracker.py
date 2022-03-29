"""This script tracks and visualises ISS's current position on a 2d map.
    It also provides the date and time of the next ISS pass at the user's location"""

# importing libraries
import json  # used for parsing json response
from tkinter import TclError
import requests  # used for sending a request to the api server
import turtle  # used for visualising the iss position
from datetime import datetime  # used for parsing unix time response from the server
import time  # pauses the API call thread for 5 seconds, saving server resources
# used for grabbing user's geographical coodrdinates
from geopy.geocoders import Nominatim

# fetching the user lon and lat
print("""Please enter your city and country details so that I can give you the date of next ISS sighting at your location.
        All of the above details are used in the script only for fetching your geographical coordinates and are not sent to/used by any third party.\n """)
geolocator = Nominatim(user_agent="iss_tracker")
city = input("Enter your city: ")
country = input("Enter your country: ")
loc = geolocator.geocode(city+',' + country)


# settting up the map window as well as the Turtle object
screen = turtle.Screen()
screen.setup(1280, 720)
# the max limits of long, lat range from -180,180 and -90,90.
screen.setworldcoordinates(-180, -90, 180, 90)
screen.bgpic("world_map_final.gif")
# iss turtle
screen.register_shape("iss.gif")
iss = turtle.Turtle()
iss.shape("iss.gif")
iss.setheading(90)
iss.penup()


# fetching the next sighting at user's location
user_lat = loc.latitude
user_lon = loc.longitude

location = turtle.Turtle()
location.speed(0)
location.hideturtle()
location.penup()
location.goto(user_lon, user_lat)
location.color("crimson")
location.dot(5)

sighting_url = f"http://api.open-notify.org/iss-pass.json?lat={str(user_lat)}&lon={str(user_lon)}"
# we will use a 'get' request to the api server and capture the response object
sighting_response = requests.get(sighting_url)


over = sighting_response.json()["response"][1]["risetime"]
# writes a text at the turtle's current location
location.write(time.ctime(over), font=("Verdana", 25, 'bold'))


# fetching the data from the open-notify api
flag = True
url = "http://api.open-notify.org/iss-now.json"

while flag:
    # we will use a 'get' request to the api server and capture the response object
    response = requests.get(url)
    # use conditional checks incase of internet/api connectivity issues
    if response.status_code != 200:
        print(
            """Either the server is experiencing problems or your internet connection is down.
                Please check your internet connection and try again""")
    else:
        position = response.json()['iss_position']  # parsing the json response
        lon = position['longitude']  # current longitude
        lat = position['latitude']  # current latitude

    iss.goto(float(lon), float(lat))
    time.sleep(5)
try:
    if screen.exitonclick() == True:  # terminates the API call loop if the user closes the map window
        flag = False
except TclError:
    pass
