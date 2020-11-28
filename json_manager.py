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
    def move_code_to_ploads(code_json, ploads_json):
        code = JsonManager.load_json_from_file(code_json)
        code = code['code']

        ploads = JsonManager.load_json_from_file(ploads_json)
        ploads['ploads']['POST_ploads']['code'] = code
        JsonManager.dump_into_json_file(ploads_json, ploads)