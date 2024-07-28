import requests
from api_key import API_KEY

BASE_URL = 'http://ws.audioscrobbler.com/2.0/'


def get_upcoming_events(artist_name, api_key):
    params = {
        'method': 'artist.getEvents',
        'artist': artist_name,
        'api_key': api_key,
        'format': 'json'
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        events = data.get('events', {}).get('event', [])
        if not events:
            print(f"No upcoming events found for artist: {artist_name}")
        else:
            for event in events:
                title = event.get('title')
                date = event.get('date')
                venue = event.get('venue', {}).get('name', 'Unknown Venue')
                location = event.get('venue', {}).get('location', {}).get('city', 'Unknown Location')
                print(f"Event: {title}")
                print(f"Date: {date}")
                print(f"Venue: {venue}")
                print(f"Location: {location}")
                print('---')
    else:
        print(f"Failed to retrieve data: Status code {response.status_code}")


if __name__ == "__main__":
    # Example usage
    artist_name = 'Metallica'
    get_upcoming_events(artist_name, API_KEY)
