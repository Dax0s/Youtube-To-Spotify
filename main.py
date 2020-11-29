import callback_server
from json_manager import JsonManager
from spotify_requests import SpotifyRequests

import requests
import webbrowser



SpotifyRequests.get_token('jsons/ploads.json', 'jsons/tokens.json')

#
# ploads = JsonManager.load_json_from_file('jsons/ploads.json')
#
# response = requests.get('https://accounts.spotify.com/authorize', params=ploads['ploads']['GET_ploads'])
# webbrowser.open(response.url)
#
# callback_server.HttpServer.start_server()
#
# ploads = JsonManager.load_json_from_file('jsons/ploads.json')
#
# response1 = requests.post('https://accounts.spotify.com/api/token', data=ploads['ploads']['POST_ploads'])
#
# print(response1.status_code)
#
# JsonManager.dump_into_json_file('jsons/response_json.json', response1.json())



# with open('response.json', 'w') as f:
#     json.dump(response1.json(), f, indent=2)