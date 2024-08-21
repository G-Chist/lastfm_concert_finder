from api_key import API_KEY
from top_artists import get_top_artists
from concerts_for_artist import get_upcoming_events
from city_distance import get_coordinates, is_within_radius
from parse_concert import convert_date, parse_events

username = "g_chist"
top_number = 50
city = "Worcester, MA"
radius_km = 100

suggested_concerts = []

top_bands_raw = get_top_artists(username, API_KEY, top_number)
print("Top bands list fetched")

top_bands = []

for idx, artist in enumerate(top_bands_raw, start=1):
    top_bands.append(artist['name'])

parse_counter = 0
for band in top_bands:

    try:
        band_concerts_links = get_upcoming_events(band)
        band_concerts = parse_events(band_concerts_links)

        for concert in band_concerts:
            concert_city = concert[1]
            if concert not in suggested_concerts:
                suggested_concerts.append(concert)

        parse_counter += 1

        print(f'{parse_counter} out of {top_number} parsed')

    except:
        print("Timeout error")

for suggested_concert in suggested_concerts:
    print(suggested_concert)
