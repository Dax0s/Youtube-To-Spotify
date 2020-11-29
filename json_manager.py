import json

class JsonManager:

    @staticmethod
    def load_json_from_string(json_name):
        return json.loads(json_name)

    @staticmethod
    def load_json_from_file(file_name):
        with open(file_name, 'r') as f:
            return json.load(f)

    @staticmethod
    def dump_into_json_string(var_name):
        return json.dumps(var_name, indent=2)

    @staticmethod
    def dump_into_json_file(file_name, var_name):
        with open(file_name, 'w') as f:
            json.dump(var_name, f, indent=2)

    @staticmethod
    def move_code_to_ploads(ploads_json, code_json):
        code = JsonManager.load_json_from_file(code_json)['code']

        ploads = JsonManager.load_json_from_file(ploads_json)
        ploads['using_code']['code'] = code
        JsonManager.dump_into_json_file(ploads_json, ploads)

    @staticmethod
    def move_ids_to_ploads(ploads_json, ids_json):
        ids = JsonManager.load_json_from_file(ids_json)
        code_ploads = JsonManager.load_json_from_file(ploads_json)['using_code']
        refresh_token_ploads = JsonManager.load_json_from_file(ploads_json)['using_refresh_token']

        code_ploads['client_id'] = ids['client_id']
        code_ploads['secret_id'] = ids['secret_id']

        refresh_token_ploads['client_id'] = ids['client_id']
        refresh_token_ploads['secret_id'] = ids['secret_id']

    @staticmethod
    def move_token_to_ploads(ploads_json, tokens_json):
        tokens = JsonManager.load_json_from_file(tokens_json)

        ploads = JsonManager.load_json_from_file(ploads_json)
        ploads['using_refresh_token']['refresh_token'] = tokens['refresh_token']
        ploads['using_access_token']['access_token'] = tokens['access_token']

        JsonManager.dump_into_json_file(ploads_json, ploads)