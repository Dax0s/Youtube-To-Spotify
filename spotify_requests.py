from json_manager import JsonManager
from callback_server import HttpServer

import requests
import webbrowser

class SpotifyRequests:

    JsonManager.move_ids_to_ploads('jsons/ploads.json', 'jsons/ids.json')

    @staticmethod
    def get_code_request(ploads_json):
        ploads = JsonManager.load_json_from_file(ploads_json)['ploads']['GET_ploads']

        response = requests.get('https://accounts.spotify.com/authorize', params=ploads)
        webbrowser.open(response.url)

        HttpServer.start_server()

    @staticmethod
    def get_token_with_code_request(ploads_json, tokens_json):
        ploads = JsonManager.load_json_from_file(ploads_json)['ploads']['POST_ploads']['code']

        response = requests.post('https://accounts.spotify.com/api/token', data=ploads)

        JsonManager.dump_into_json_file(tokens_json, response.json())
        JsonManager.move_token_to_ploads(ploads_json, tokens_json)

    @staticmethod
    def get_token_with_refresh_token(ploads_json, tokens_json):
        ploads = JsonManager.load_json_from_file(ploads_json)['ploads']['POST_ploads']['token']

        response = requests.post('https://accounts.spotify.com/api/token', data=ploads)

        if 'refresh_token' in response.json().keys():
            JsonManager.dump_into_json_file(tokens_json, response.json())
        else:
            response_dict = response.json()
            response_dict['refresh_token'] = ploads['refresh_token']

            JsonManager.dump_into_json_file(tokens_json, response_dict)

        JsonManager.move_token_to_ploads(ploads_json, tokens_json)


    @staticmethod
    def get_token(ploads_json, tokens_json):
        ploads = JsonManager.load_json_from_file(ploads_json)['ploads']['POST_ploads']

        if ploads['token']['refresh_token'] != "":
            SpotifyRequests.get_token_with_refresh_token(ploads_json, tokens_json)
        else:
            SpotifyRequests.get_code_request(ploads_json)
            SpotifyRequests.get_token_with_code_request(ploads_json, tokens_json)