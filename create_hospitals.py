from geopy.geocoders import Nominatim
import folium

user_agent = "geoapiExercises/1.0 AIzaSyBIeklfsRu1yz97lY2gJzWHJcmrd7lx2zU"

# Initialize the geocoder with the user agent
geolocator = Nominatim(user_agent=user_agent, timeout=10)
# List of locations to geocode
locations = ["Denver, CO, United States", "New York, NY, United States", "Los Angeles, CA, United States"]

# Create an empty map
map_location = folium.Map(location=[0, 0], zoom_start=5)

# Iterate through the list of locations
for location in locations:
    # Perform geocoding
    location_info = geolocator.geocode(location)

    if location_info:
        # Extract latitude and longitude
        latitude = location_info.latitude
        longitude = location_info.longitude

        # Add a marker for the geocoded location
        folium.Marker([latitude, longitude], popup=location).add_to(map_location)
    else:
        print(f"Geocoding was not successful for the location: {location}")

# Save or display the map (as an HTML file)
map_location.save("geocoded_locations_map.html")

print("Map created and saved as 'geocoded_locations_map.html'")
