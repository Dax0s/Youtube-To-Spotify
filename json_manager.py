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
        ploads['ploads']['POST_ploads']['code']['code'] = code
        JsonManager.dump_into_json_file(ploads_json, ploads)

    @staticmethod
    def move_ids_to_ploads(ploads_json, ids_json):
        ids = JsonManager.load_json_from_file(ids_json)
        ploads = JsonManager.load_json_from_file(ploads_json)['ploads']['POST_ploads']

        ploads['code']['client_id'] = ids['client_id']
        ploads['code']['secret_id'] = ids['secret_id']

        ploads['token']['client_id'] = ids['client_id']
        ploads['token']['secret_id'] = ids['secret_id']

    @staticmethod
    def move_token_to_ploads(ploads_json, tokens_json):
        token = JsonManager.load_json_from_file(tokens_json)['refresh_token']

        ploads = JsonManager.load_json_from_file(ploads_json)
        ploads['ploads']['POST_ploads']['token']['refresh_token'] = token

        JsonManager.dump_into_json_file(ploads_json, ploads)