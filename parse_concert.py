import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

BASE_URL = 'https://www.last.fm/'


def convert_date(date_string):
    # Regex to match date format and separate time if present
    date_pattern = r'(\w+ \d{1,2} \w+ \d{4})'
    match = re.search(date_pattern, date_string)

    if match:
        # Extract day of the week and date string
        full_date = match.group(1)

        # Convert the date string into a datetime object
        date_obj = datetime.strptime(full_date, '%A %d %B %Y')

        # Extract the day of the week
        day = date_obj.strftime('%A')

        # Convert to MM/DD/YYYY format
        date = date_obj.strftime('%m/%d/%Y')

        return day, date
    else:
        return None, None


def parse_events(links):

    dates = []
    days = []
    lineups = []
    cities = []
    venues = []

    for link in links:

        url = BASE_URL + link
        lineup_link = url + '/lineup'
        response = requests.get(url)
        response_lineup = requests.get(lineup_link)
        html_content = response.content
        html_content_lineup = response_lineup.content
        soup = BeautifulSoup(html_content, 'html.parser')
        soup_lineup = BeautifulSoup(html_content_lineup, 'html.parser')

        address_locality = soup.find('span', itemprop='addressLocality')
        locality_text = address_locality.get_text()
        cities.append(locality_text)

        venue_tag = soup.find('strong', itemprop='name')
        venue_text = venue_tag.get_text()
        venues.append(venue_text)

        start_date_element = soup.find(itemprop='startDate')
        date_text = start_date_element.get_text(strip=True)
        day, date = convert_date(date_text)
        days.append(day)
        dates.append(date)

    return cities, venues, days, dates


if __name__ == "__main__":
    links = ['/event/4846117+Silver+Scream+Con-cert', '/event/4682903+METALLICA+-+M72+World+Tour', '/event/4682906+Metallica+-+M72+World+Tour', '/event/4816345+Ice+Nine+Kills+at+The+Backyard+on+03+September+2024', '/event/4846117+Silver+Scream+Con-cert', '/event/4682752+Metallica+at+Estadio+GNP+Seguros+on+22+September+2024', '/event/4682762+Metallica+at+Estadio+GNP+Seguros+on+29+September+2024', '/event/4820116+The+Amity+Affliction+at+Riverstage+on+08+November+2024', '/event/4820532+The+Amity+Affliction+at+Hordern+Pavilion+on+09+November+2024', '/event/4820144+The+Amity+Affliction', '/event/4823272+Let+The+Ocean+Take+Me+-+10+Year+Anniversary+Tour', '/event/4845169+The+Amity+Affliction']
    events_parsed = parse_events(links)
    print(events_parsed)
