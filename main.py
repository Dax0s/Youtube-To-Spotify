from spotify_requests import SpotifyRequests
from json_manager import JsonManager


ploads_json, tokens_json, playlists_json, user_info_json = 'jsons/ploads.json', 'jsons/tokens.json', 'jsons/users_playlists.json', 'jsons/user_info.json'


SpotifyRequests.get_token(ploads_json, tokens_json)

SpotifyRequests.get_user_info(tokens_json, user_info_json)
SpotifyRequests.check_if_a_playlist_exists(ploads_json, playlists_json, "Chill")