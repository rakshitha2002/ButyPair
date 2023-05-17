import os
import requests


def getColorAPIData(api_url):
    error_count = 0
    while True:
        try:
            print(f"INFO  :: Fetching color data from {api_url}")
            response  = requests.get(api_url)
            if response.status_code == 200:
                return response
            else:
                print(f"ERROR :: {api_url} failed")
                error_count += 1
        except Exception as e:
            error_count += 1

        if error_count > 10:
            raise Exception("ERROR :: COLOR API FAILED")


def rrmdir(path):
    for entry in os.scandir(path):
        if entry.is_dir():
            rrmdir(entry)
        else:
            os.remove(entry)
    os.rmdir(path)