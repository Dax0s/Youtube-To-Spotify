from spotify_requests import SpotifyRequests
from json_manager import JsonManager


ploads_json, tokens_json, playlists_json, user_info_json = 'jsons/ploads.json', 'jsons/tokens.json', 'jsons/users_playlists.json', 'jsons/user_info.json'


SpotifyRequests.get_token(ploads_json, tokens_json)

# for i in range(50):
#     SpotifyRequests.create_a_playlist(ploads_json, user_info_json, playlists_json, f"Test Playlist {i + 1}")

# for i in range(50):
#     SpotifyRequests.unfollow_user_playlist(ploads_json, playlists_json, f"Test Playlist {i + 1}")

# SpotifyRequests.unfollow_user_playlist(ploads_json, playlists_json, "Test Playlist 1")

SpotifyRequests.print_user_playlists(ploads_json, playlists_json)