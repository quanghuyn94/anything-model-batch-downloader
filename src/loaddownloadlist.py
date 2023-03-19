import json
def load_download_list(json_str) -> dict:
    download_list = json.loads(json_str)
    return download_list
