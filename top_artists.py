from api_key import API_KEY
import requests

USER = 'g_chist'  # Replace with the Last.fm username
LIMIT = 300  # The number of top artists to fetch


def get_top_artists(user, api_key, limit=300):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.gettopartists',
        'user': user,
        'api_key': api_key,
        'format': 'json',
        'limit': limit
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return f"Failed to retrieve data: Status code {response.status_code}"

    data = response.json()
    if 'topartists' not in data:
        return "No top artists found for the user."

    top_artists = data['topartists']['artist']
    return top_artists


if __name__ == "__main__":
    # Example usage
    top_artists = get_top_artists(USER, API_KEY, LIMIT)
    if isinstance(top_artists, list):
        for idx, artist in enumerate(top_artists, start=1):
            print(f"{idx}. {artist['name']} - {artist['playcount']} plays")
    else:
        print(top_artists)
