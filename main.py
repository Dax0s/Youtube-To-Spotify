import callback_server
import json_manager

import json
import requests
import webbrowser


ploads = json_manager.JsonManager.load_json_from_file('jsons/ploads.json')
ids = json_manager.JsonManager.load_json_from_file('jsons/ids.json')

response = requests.get('https://accounts.spotify.com/authorize', params=ploads['ploads']['GET_ploads'])
webbrowser.open(response.url)
callback_server.HttpServer.start_server()


# response1 = requests.post('https://accounts.spotify.com/api/token', data=ploads)
#
# print(response1.status_code)
#
# with open('response.json', 'w') as f:
#     json.dump(response1.json(), f, indent=2)
