from geopy.geocoders import Photon
from geopy.distance import geodesic

# Initialize the geocoder
geolocator = Photon(user_agent="geoapiExercises")


# Function to get coordinates for a city
def get_coordinates(city):
    location = geolocator.geocode(city)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None


# Function to check if city2 is within a certain radius from city1
def is_within_radius(city1, city2, radius_km):
    coords1 = get_coordinates(city1)
    coords2 = get_coordinates(city2)
    if coords1 and coords2:
        distance = geodesic(coords1, coords2).kilometers
        return distance <= radius_km
    else:
        return False


if __name__ == "__main__":
    # Example cities and radius
    city1 = 'Worcester, MA'
    city2 = 'Hartford, CT'
    radius_km = 100
    if is_within_radius(city1, city2, radius_km):
        print(f"{city1} is within {radius_km} km of {city2}")
    if not is_within_radius(city1, city2, radius_km):
        print(f"{city1} is NOT within {radius_km} km of {city2}")

