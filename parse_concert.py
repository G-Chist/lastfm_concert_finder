import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

BASE_URL = 'https://www.last.fm'


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


def parse_events(links_list):

    dates = []
    days = []
    lineups = []
    cities = []
    venues = []

    concerts = []

    for link in links_list:

        url = BASE_URL + link
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        okay_message = 'OK'
        print(f'Status code: {status_code if status_code != 200 else okay_message}')
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
            if band_elements:
                for element in band_elements:
                    band_name = element.find('a').get_text(strip=True)
                    lineup += band_name
                    lineup += " / "
                    lineup_counter += 1

                if lineup_number > lineup_counter:
                    lineup += "more bands"
                else:
                    lineup = lineup[:-3]
        else:
            lineup = "N/A"

        lineups.append(lineup)

        concerts.append([date, locality_text, venue_text, day, lineup])

    # Remove duplicates while preserving order using list comprehension
    unique_concerts = []
    [unique_concerts.append(x) for x in concerts if x not in unique_concerts]

    return unique_concerts


if __name__ == "__main__":
    # Example usage
    links = ['/event/4846117+Silver+Scream+Con-cert', '/event/4682903+METALLICA+-+M72+World+Tour', '/event/4682906+Metallica+-+M72+World+Tour', '/event/4816345+Ice+Nine+Kills+at+The+Backyard+on+03+September+2024', '/event/4846117+Silver+Scream+Con-cert', '/event/4682752+Metallica+at+Estadio+GNP+Seguros+on+22+September+2024', '/event/4682762+Metallica+at+Estadio+GNP+Seguros+on+29+September+2024', '/event/4820116+The+Amity+Affliction+at+Riverstage+on+08+November+2024', '/event/4820532+The+Amity+Affliction+at+Hordern+Pavilion+on+09+November+2024', '/event/4820144+The+Amity+Affliction', '/event/4823272+Let+The+Ocean+Take+Me+-+10+Year+Anniversary+Tour', '/event/4845169+The+Amity+Affliction']
    events_parsed = parse_events(links)
    for event in events_parsed:
        print(event)
