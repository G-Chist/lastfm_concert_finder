import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.last.fm/music/'

def get_upcoming_events(artist_name):
    url = BASE_URL + artist_name + '/+events'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    music_events = soup.find_all(attrs={"itemtype": "http://schema.org/MusicEvent"})
    return music_events

if __name__ == "__main__":
    # Example usage
    artist_name = 'Omerta'
    events = get_upcoming_events(artist_name)
    print(events)

