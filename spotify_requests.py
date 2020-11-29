from json_manager import JsonManager
from callback_server import HttpServer

import requests
import webbrowser

class SpotifyRequests:

    JsonManager.move_ids_to_ploads('jsons/ploads.json', 'jsons/ids.json')

    @staticmethod
    def get_code(ploads_json):
        ploads = JsonManager.load_json_from_file(ploads_json)['GET_code']

        response = requests.get('https://accounts.spotify.com/authorize', params=ploads)
        print(f"get_code {response.status_code:23}")

        webbrowser.open(response.url)

        HttpServer.start_server()

    @staticmethod
    def get_token_with_code(ploads_json, tokens_json):
        ploads = JsonManager.load_json_from_file(ploads_json)['using_code']

        response = requests.post('https://accounts.spotify.com/api/token', data=ploads)
        print(f"get_token_with_code {response.status_code:12}")

        JsonManager.dump_into_json_file(tokens_json, response.json())
        JsonManager.move_token_to_ploads(ploads_json, tokens_json)

    @staticmethod
    def get_token_without_code(ploads_json, tokens_json):
        SpotifyRequests.get_code(ploads_json)
        SpotifyRequests.get_token_with_code(ploads_json, tokens_json)

    @staticmethod
    def get_token_with_refresh_token(ploads_json, tokens_json):
        ploads = JsonManager.load_json_from_file(ploads_json)['using_refresh_token']

        response = requests.post('https://accounts.spotify.com/api/token', data=ploads)
        print(f"get_token_with_refresh_token {response.status_code}")

        if 'refresh_token' in response.json().keys():
            JsonManager.dump_into_json_file(tokens_json, response.json())
        else:
            response_dict = response.json()
            response_dict['refresh_token'] = ploads['refresh_token']

            JsonManager.dump_into_json_file(tokens_json, response_dict)

        JsonManager.move_token_to_ploads(ploads_json, tokens_json)


    @staticmethod
    def get_token(ploads_json, tokens_json):
        token = JsonManager.load_json_from_file(ploads_json)['using_refresh_token']['refresh_token']

        if token != "":
            SpotifyRequests.get_token_with_refresh_token(ploads_json, tokens_json)
        else:
            SpotifyRequests.get_token_without_code(ploads_json, tokens_json)

    @staticmethod
    def get_user_info(ploads_json, user_info_json):
        token = {"access_token": JsonManager.load_json_from_file(ploads_json)['access_token'], "limit": 50}

        response = requests.get('https://api.spotify.com/v1/me', params=token)
        print(f"get_user_info {response.status_code:18}")

        JsonManager.dump_into_json_file(user_info_json, response.json())

    @staticmethod
    def get_user_playlists(ploads_json, playlists_json):
        ploads = JsonManager.load_json_from_file(ploads_json)['using_access_token']

        response = requests.get('https://api.spotify.com/v1/me/playlists', params=ploads)
        print(f"get_users_playlists {response.status_code:12}")

        JsonManager.dump_into_json_file(playlists_json, response.json())

    @staticmethod
    def check_if_a_playlist_exists(ploads_json, playlists_json, playlist_name):
        SpotifyRequests.get_user_playlists(ploads_json, playlists_json)

        playlists = JsonManager.load_json_from_file(playlists_json)

        exists = False
        for playlist in playlists['items']:
            name = playlist['name']

            if playlist_name == name:
                exists = True

        print(exists)
        return exists

    @staticmethod
    def create_a_playlist(playlists_json, playlist_name):
        if SpotifyRequests.check_if_a_playlist_exists(playlists_json, playlist_name):
            print("Playlist already exists")
            return None

