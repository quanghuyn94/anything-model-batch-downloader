
import json
import os
import requests
from . import utilis
from . import downloadmanager
from modules import simpleargument
import re

model_info = "https://civitai.com/api/v1/models/"

save_dict = [""]
extesion = [".safetensors", ".ckpt", ".pt"]

def get_model_info_from_id(model_id : str) -> dict:
    respone = requests.get(f"{model_info}{model_id}")
    json_str = respone.content.decode("utf-8")
    json_data = json.loads(json_str)

    return json_data

def get_model_download_list(model_info : dict):
    file_infos = utilis.find_values("files", model_info)["files"]
    model_download_list = []
    for clean_file_info in file_infos:
        model_download_list.append({
            "name" : clean_file_info[0]["name"], 
            "type" : clean_file_info[0]['type'],
            "downloadUrl" : clean_file_info[0]["downloadUrl"]})

    return model_download_list

def get_id_from_url(url : str):
    match = re.search(r'\d+', url)
    if match:
        number = match.group()
        return number
    else:
        print("No id found in the URL")
        return 0
def get_type(model_info : dict):
    model_types = utilis.find_values("type", model_info)
    model_type : str = model_types["type"][0]

    return model_type.lower()
def download_now(model_url : str, args : str):
    sa = simpleargument.SimpleArguments()
    
    sa.parser(args)

    model_id = get_id_from_url(model_url)

    if model_id != 0:
        model_info = get_model_info_from_id(model_id)

        model_download_list = get_model_download_list(model_info)

        if sa.get_argument("skip-vae"):
            vae_download_link = get_vae_download_link(model_download_list, sa.get_argument("vae-ver"))
            downloadmanager.download(vae_download_link[2], vae_download_link[0])


        model_download_link = get_model_download_link(model_download_list, sa.get_argument("model-ver"))
        downloadmanager.download(model_download_link[2], model_download_link[0])

def get_vae_download_link(model_download_list : dict, ver):
    vae_links = []

    for model in model_download_list:
        if ver:
            if ver in model["name"]:
                print(f'Download ver {model["name"]}')
                vae_links.append((model["name"], model["type"], model["downloadUrl"]))
                break
        else:
            if model["name"].endswith(".vae.pt"):
                vae_links.append((model["name"], model["type"], model["downloadUrl"]))

    latest_vae_link = vae_links[0] if vae_links else None

    return latest_vae_link

def get_model_download_link(model_download_list : dict, ver: str = None):

    safetensors_links = []
    latest_safetensors_link = ""

    for model in model_download_list:
        if ver:
            if ver in model["name"] and "vae" not in model["name"]:
                print(f'Download ver {model["name"]}')
                safetensors_links.append((model["name"], model["type"], model["downloadUrl"]))
                break
        elif "vae" not in model["name"]:
            safetensors_links.append((model["name"], model["type"], model["downloadUrl"]))

    latest_safetensors_link = safetensors_links[0] if safetensors_links else None

    return latest_safetensors_link
    
