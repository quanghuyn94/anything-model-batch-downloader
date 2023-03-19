import requests

def download(url : str, file_path : str):
    print(f"Download... {file_path} from {url}")
    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)
    print(f"Download {file_path} from {url} done!")
