import json
from src import utilis, civitaihelper, downloadmanager, loaddownloadlist
from modules.simpleargument import SimpleArguments
from argparse import ArgumentParser
import os

config = {
    "checkpoint" : "models/Stable-diffusion",
    "vae": "models/VAE",
    "lora": "models/Lora",
    "ControlNet": "models/ControlNet",
    "textualinversion" : "embeddings",
    "hypernetworks" : "models/hypernetworks"
}

sa = SimpleArguments()
    
def argument_parse():
    parser = ArgumentParser()
    # parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--listpath', type=str, default="download_list.json", help="Path to download_list.json")
    parser.add_argument('--savepath', type=str, default="", help="Path to save folder")
    parser.add_argument('--configpath', type=str, default='config.json', help="Path to custom config.json")
    parser.add_argument('--helparg', action="store_true", help="Show all string arguments")
    args = parser.parse_args()

    return args

def create_save_dir(file_name : str, save_path : str, model_type : str, create_sub = False):
    save_sub_path = ""
    if create_sub:
        save_sub_path = file_name[:file_name.rfind(".")]

    save_dir = os.path.join(save_path, model_type, save_sub_path)
    os.makedirs(save_dir, exist_ok=True)

    return os.path.join(save_dir, file_name)

def civitai_download(save_path, model_url : str):
    model_id = civitaihelper.get_id_from_url(model_url)

    if model_id != 0:
        model_info = civitaihelper.get_model_info_from_id(model_id)

        model_download_list = civitaihelper.get_model_download_list(model_info)

        model_type = civitaihelper.get_type(model_info) 
        if sa.get_argument("type"):
            model_type = sa.get_argument("type")

        if sa.get_argument("skip-vae") == False and model_type == "checkpoint":
            vae_download_link = civitaihelper.get_vae_download_link(model_download_list, sa.get_argument("vaever"))
            if vae_download_link is not None:
                model_save_path = create_save_dir(vae_download_link[0], save_path, config["vae"], False)

                if sa.get_argument("saveto"):
                    model_save_path = os.path.join(sa.get_argument("saveto"), model_download_link[0])

                if sa.get_argument("forceoverwrite") or os.path.exists(model_save_path) == False:
                    if sa.get_argument("forceoverwrite"):
                        print("force-overwrite", vae_download_link[2])
                    downloadmanager.download(vae_download_link[2], model_save_path)
                else:
                    print("Skip", vae_download_link[2])
            else:
                print("No VAE to download.")

        model_download_link = civitaihelper.get_model_download_link(model_download_list, sa.get_argument("modelver"))
        model_save_path = create_save_dir(model_download_link[0], save_path, config[model_type], sa.get_argument("sub"))

        if sa.get_argument("saveto"):
                print("Save model to", sa.get_argument("saveto"))
                model_save_path = os.path.join(sa.get_argument("saveto"), model_download_link[0])

        if sa.get_argument("forceoverwrite") or os.path.exists(model_save_path) == False:
            if sa.get_argument("forceoverwrite"):
                print("force-overwrite", model_download_link[2])

            downloadmanager.download(model_download_link[2], model_save_path)
        else:
            print("Skip", model_download_link[2])

def main():
    global config
    
    program_args = argument_parse()

    if program_args.helparg:
        SimpleArguments.print_help("simple_args_help.json")
        return
    
    if os.path.exists(program_args.configpath):
        with open(program_args.configpath, 'r') as f:
            config = json.loads(f.read())
    else:
        with open("config.json", "w") as f:
            f.write(json.dumps(config))

    save_path = program_args.savepath

    json_str = ""

    with open(program_args.listpath, 'r') as f:
        json_str = f.read()

    print("Warmup, the download is in progress.")

    model_list = loaddownloadlist.load_download_list(json_str)["urls"]
    print(f"Download {str(model_list)}")
          
    for model in model_list:
        sa.clear()
        args = ""
        if "args" in model:
            args = model["args"]
        
        model_url = model["model_url"]
        
        sa.parser(args)
        print(sa.args)
        if sa.get_argument("skip"):
            print("Skip", model_url)
            continue
        
        if sa.get_argument("raw"):
            
            model_save_path = create_save_dir(sa.get_argument("raw"), save_path, config[sa.get_argument("type")], sa.get_argument("sub"))

            if sa.get_argument("saveto"):
                model_save_path = os.path.join(sa.get_argument("saveto"), sa.get_argument("raw"))

            if sa.get_argument("forceoverwrite") or os.path.exists(model_save_path) == False:
                if sa.get_argument("forceoverwrite"):
                    print("force-overwrite", model_url)
                downloadmanager.download(model_url, model_save_path)
            else:
                print("Skip", model_url)
        else:
            civitai_download(save_path, model_url)
            

if __name__ == "__main__":
    main()