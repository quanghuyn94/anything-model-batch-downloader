# Introduce

- Anything Model Batch Downloader allows you to batch download models from civitai, hugging face easily just through model url.
- Anything Model Bacth Downloader is designed to run on cloud systems like Google Colab, Amazon SageMaker. 

# Feature
## Batch download:
- The download will be done via a json file.
## Arguments System:
- The arguments system allows you to add download conditions to the downloader.
## Easy Expansion:
- Anything Model Batch Download is written as modules, allowing you to use the source code in a simpler way.
# Use
### First, you need to have a download list file in JSON format, it should look like this:
```json
{
    "urls" : [
        {
            "model_url": "https://civitai.com/models/2583/grapefruit-hentai-model"
        },
        {
            "model_url" : "https://civitai.com/models/11367/tifameenow",
            "args" : "sub"
        },
        {
            "model_url" : "https://civitai.com/api/download/models/12477",
            "args" : "raw=\"arknights-suzuran.safetensors\" type=\"lora\" sub forcerewrite"
        },
        {
            "model_url" : "https://civitai.com/models/4514/pure-eros-face",
            "args" : "sub saveto=\"nsfw\""
        }
    ]
}
```
In there:
- `model_url` is the download link.
- `args` are the conditions required for the download.
### Run:
```bash
python batch_download.py
```
Or if you have a custom json file:
```bash
python batch_download.py --listpath="you/path/to/json"
```

# Arguments:
| Arguments     | Info |
|---------------| ----------|
| --listpath | Path to download_list.json. |
| --savepath | Path to save folder. |
| --configpath | Path to custom config.json. |
| --helparg | Show all downloader arguments. |

| Downloader Arguments     | Info |
|---------------| ----------|
| sub | Create a subfolder after downloading. |
| skip | Skip current download link. |
| skipvae | Skip the vae download.|
| raw=RAW | Download raw url, raw url is a download link. Requires an input argument that is the name of the file. |
| forceoverwrite | Overwrite downloaded files. |
| vaever=VAEVER| Specify a vae version. |
| modelver=MODELVER | Specify a model version |
| type=TYPE | Model type.|
| saveto=SAVETO | Specify a special save path.|

# Have fun (●'◡'●).
