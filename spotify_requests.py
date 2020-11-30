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
        ploads = JsonManager.load_json_from_file(ploads_json)['using_access_token']

        response = requests.get('https://api.spotify.com/v1/me', params=ploads)
        print(f"get_user_info {response.status_code:18}")

        JsonManager.dump_into_json_file(user_info_json, response.json())
        JsonManager.move_user_id_to_ploads(ploads_json, user_info_json)

    @staticmethod
    def get_user_playlists(ploads_json, playlist_json):
        ploads = JsonManager.load_json_from_file(ploads_json)['using_access_token']

        response = requests.get('https://api.spotify.com/v1/me/playlists', params=ploads)
        print(f"get_users_playlists {response.status_code:12}")

        JsonManager.dump_into_json_file(playlist_json, response.json())

    @staticmethod
    def check_if_a_playlist_exists(ploads_json, playlist_json, playlist_name):
        SpotifyRequests.get_user_playlists(ploads_json, playlist_json)

        playlists = JsonManager.load_json_from_file(playlist_json)

        exists = False
        for playlist in playlists['items']:
            name = playlist['name']

            if playlist_name == name:
                exists = True

        return exists

    @staticmethod
    def create_a_playlist(ploads_json, user_info_json, playlist_json, playlist_name):
        if SpotifyRequests.check_if_a_playlist_exists(ploads_json, playlist_json, playlist_name):
            print("Playlist already exists")
            return None

        SpotifyRequests.get_user_info(ploads_json, user_info_json)

        ploads = JsonManager.load_json_from_file(ploads_json)
        user_id = ploads['using_access_token']['user_id']
        ploads['create_playlist_body']['name'] = playlist_name

        data = JsonManager.dump_into_json_string(ploads['create_playlist_body'])
        headers = ploads['using_authorization_token']

        response = requests.post(f'https://api.spotify.com/v1/users/{user_id}/playlists', data=data, headers=headers)
        print(f"create_a_playlist {response.status_code:14}")

    @staticmethod
    def print_user_playlists(ploads_json, playlist_json):
        SpotifyRequests.get_user_playlists(ploads_json, playlist_json)

        playlists = JsonManager.load_json_from_file(playlist_json)

        for i in range(len(playlists['items'])):
            print((i + 1), playlists['items'][i]['name'])

    @staticmethod
    def get_user_playlist(ploads_json, playlist_json, playlist_name):
        if False == SpotifyRequests.check_if_a_playlist_exists(ploads_json, playlist_json, playlist_name):
            print("Error: Playlist doesn't exist")
            return None

        playlists = JsonManager.load_json_from_file(playlist_json)

        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                JsonManager.dump_into_json_file('jsons/playlist.json', playlist)

                return playlist

    @staticmethod
    def unfollow_user_playlist(ploads_json, playlist_json, playlist_name):
        if False == SpotifyRequests.check_if_a_playlist_exists(ploads_json, playlist_json, playlist_name):
            print("Error: Playlist doesn't exist")
            return None

        playlist = SpotifyRequests.get_user_playlist(ploads_json, playlist_json, playlist_name)
        ploads = JsonManager.load_json_from_file(ploads_json)['using_authorization_token']

        playlist_id = playlist['id']

        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/followers'
        headers = ploads

        response = requests.delete(url, headers=headers)