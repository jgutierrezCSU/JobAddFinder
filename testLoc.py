#  '5b3ce3597851110001cf624848c4d06805944a2b845f364ecdfec406'  
import requests
from pytotal import Nominatim
from geopy import distance

# Set up the OpenRouteService API endpoint and API key
openroute_api = "https://api.openrouteservice.org/api/1.0/route?"
api_key = "5b3ce3597851110001cf624848c4d06805944a2b845f364ecdfec406"

# Set up the Nominatim endpoint and API key
nominatim_api = "https://nominatim.openstreetmap.org/api/0.1/"
nominatim_api_key = "YOUR_API_KEY_HERE"

# Define the start and end points for the journey
start_point = "Stuttgart, Germany"
end_point = "Weinsberg, Germany"

# Use Nominatim to geocode the start and end points
nominatim = Nominatim(nominatim_api, api_key=nominatim_api_key)
start_point_coords = nominatim.geocode(start_point)[0]
end_point_coords = nominatim.geocode(end_point)[0]

# Calculate the distance using OpenRouteService API
response = requests.get(openroute_api, params={
    "api_key": api_key,
    "coords": f"{start_point_coords[0]}, {start_point_coords[1]}",
    "type": "public_transport"
})

# Extract the travel time from the response
travel_time_public_transport = response.json()["routes"][0]["duration"]

# Calculate the distance using geopy
distance_km = distance.vincenty(start_point_coords, end_point_coords).km

# Calculate the driving time using the distance and a speed of 60 km/h
driving_time = distance_km / 60

print(f"Travel time by public transport: {travel_time_public_transport} minutes")
print(f"Driving distance: {distance_km} km")
print(f"Driving time: {driving_time} minutes")