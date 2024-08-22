from api_key import API_KEY
from top_artists import get_top_artists
from concerts_for_artist import get_upcoming_events
from city_distance import get_coordinates, is_within_radius
from parse_concert import convert_date, parse_events

username = "g_chist"
top_number = 100
city = "Worcester, MA"
radius_km = 100

band = 'The Devil Wears Prada'

band_concert_links = get_upcoming_events(band)

print("Concert links: ")
for link in band_concert_links:
    print(link)

print()

band_concerts = parse_events(band_concert_links)

print("Concerts: ")
for concert in band_concerts:
    print(concert)
    
