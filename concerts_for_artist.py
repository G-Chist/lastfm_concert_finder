import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.last.fm/'


def get_upcoming_events(artist_name):
    artist = artist_name.replace(" ", "+")
    url = BASE_URL + 'music/' + artist + '/+events'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    music_events = soup.find_all(attrs={"itemtype": "http://schema.org/MusicEvent"})
    links = []
    for event in music_events:
        event_link = event.find(class_="events-list-item-event-name link-block-target")
        href = event_link.get('href')
        links.append(href)
    return links


if __name__ == "__main__":
    # Example usage
    artist_name = 'Ice Nine Kills'
    events = get_upcoming_events(artist_name)
    print(events)

