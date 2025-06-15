import requests
import time
import os

def check_path_type(path):
    if os.path.isfile(path):
        return "file"
    elif os.path.isdir(path):
        return "directory"
    else:
        return "not found"
def isvirus(path):
    API_KEY = '0559c6c1b798416ecefb8ee8da0a3c56dcbaf20aa3ce43e349165a2974079062'
    file_path = path

    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f)}
        headers = {"x-apikey": API_KEY}
        response = requests.post('https://www.virustotal.com/api/v3/files', files=files, headers=headers)

    if response.status_code != 200:
        print("Upload failed")
        exit()

    analysis_id = response.json()['data']['id']

    analysis_url = f'https://www.virustotal.com/api/v3/analyses/{analysis_id}'

    while True:
        response = requests.get(analysis_url, headers=headers)
        data = response.json()

        status = data['data']['attributes']['status']
        if status == 'completed':
            stats = data['data']['attributes']['stats']
            malicious = stats.get('malicious', 0)
            suspicious = stats.get('suspicious', 0)

            if malicious > 0 or suspicious > 0:
                return True   # Infected
            else:
                return False  # Clean
        else:
            time.sleep(2)
def list_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        return []
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def scan_folder_for_viruses(folder_path):
    if check_path_type(folder_path) == "file":
        return isvirus(folder_path)

    for root, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            print(f"Scanning: {full_path}")
            if isvirus(full_path):
                print(f"Infected file found: {full_path}")
                return True

    print("No infected files found.")
    return False