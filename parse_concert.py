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
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        address_locality = soup.find('span', itemprop='addressLocality')
        if address_locality:
            locality_text = address_locality.get_text()
        else:
            locality_text = "N/A"
        cities.append(locality_text)

        venue_tag = soup.find('strong', itemprop='name')
        if venue_tag:
            venue_text = venue_tag.get_text()
        else:
            venue_text = "N/A"
        venues.append(venue_text)

        start_date_element = soup.find(itemprop='startDate')
        if start_date_element:
            date_text = start_date_element.get_text(strip=True)
            day, date = convert_date(date_text)
        else:
            day = "N/A"
            date = "N/A"
        days.append(day)
        dates.append(date)

        lineup = ""
        lineup_counter = 0
        lineup_section = soup.find('section', id='line-up')
        if lineup_section:
            lineup_text = lineup_section.find('h2').get_text(strip=True)
            lineup += lineup_text
            lineup += ": "

            # Use regular expression to find the number within parentheses
            match = re.search(r'\((\d+)\)', lineup)

            if match:
                # Extract the number (group 1)
                lineup_number = int(match.group(1))


            band_elements = soup.find_all('p', class_='grid-items-item-main-text', itemprop='name')
            for element in band_elements:
                band_name = element.find('a').get_text(strip=True)
                lineup += band_name
                lineup += " / "
                lineup_counter += 1

            if lineup_number < lineup_counter:
                lineup += " / more bands"
        else:
            lineup = "N/A"

        lineup = lineup[:-3]

        lineups.append(lineup)

    return cities, venues, days, dates, lineups


if __name__ == "__main__":
    links = ['/event/4846117+Silver+Scream+Con-cert', '/event/4682903+METALLICA+-+M72+World+Tour', '/event/4682906+Metallica+-+M72+World+Tour', '/event/4816345+Ice+Nine+Kills+at+The+Backyard+on+03+September+2024', '/event/4846117+Silver+Scream+Con-cert', '/event/4682752+Metallica+at+Estadio+GNP+Seguros+on+22+September+2024', '/event/4682762+Metallica+at+Estadio+GNP+Seguros+on+29+September+2024', '/event/4820116+The+Amity+Affliction+at+Riverstage+on+08+November+2024', '/event/4820532+The+Amity+Affliction+at+Hordern+Pavilion+on+09+November+2024', '/event/4820144+The+Amity+Affliction', '/event/4823272+Let+The+Ocean+Take+Me+-+10+Year+Anniversary+Tour', '/event/4845169+The+Amity+Affliction']
    events_parsed = parse_events(links)
    print(events_parsed)
