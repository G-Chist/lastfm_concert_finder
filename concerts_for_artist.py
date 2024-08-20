import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.last.fm/'


def get_upcoming_events(artist_name):
    artist = artist_name.replace(" ", "+")
    url = BASE_URL + 'music/' + artist + '/+events'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    response = requests.get(url, headers=headers)
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

