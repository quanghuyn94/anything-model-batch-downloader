import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.realpath(__file__))

import unittest
from src import civitaihelper

class CivitaihelperTest(unittest.TestCase):
    def test_get_model_id(self):
        print(civitaihelper.get_id_from_url("https://civitai.com/models/2583/grapefruit-hentai-model"))
        print("Pass!")

    def test_get_model_download_list(self):
        model_info = civitaihelper.get_model_info_from_id("2583")
        print(civitaihelper.get_model_download_list(model_info))
        print("Pass!")

    def test_model_download_now(self):
        civitaihelper.download_now("https://civitai.com/models/2583/grapefruit-hentai-model", "ver=\"grapefruitv32\"")
        print("Pass!")

    def test_model_type_now(self):
        model_info = civitaihelper.get_model_info_from_id("8484")
        civitaihelper.get_type("https://civitai.com/models/2583/grapefruit-hentai-model", "ver=\"grapefruitv32\"")
        print("Pass!")

if __name__ == "__main__":
    unittest.main()

