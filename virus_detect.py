import requests
import os
import time 
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
        files = {'file': (file_path, open(file_path, 'rb'))}
        params = {'apikey': API_KEY}
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)


    if response.status_code != 200:
        print("Upload failed")
        exit()

    analysis_id = response.json()['scan_id']

    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {
        'apikey': API_KEY,
        'resource': analysis_id  
    }

    while True:
        response = requests.get(url, params=params)

        # Check if there is a response
        if response.status_code != 200:
            print("Failed to get report or empty response, retrying...")
            time.sleep(10)

            continue

        try:
            data = response.json()
        except Exception as e:
            print(f"Failed to decode JSON: {e}")
            continue

        if data.get('response_code') == 1:
            malicious = data.get('positives', 0)
            total = data.get('total', 0)

            if malicious > 0:
                print(f"Virus detected! {malicious} / {total} engines flagged this file.")
                return True
            else:
                print("No virus detected.")
                return False
        else:
            print("Report not ready yet")
            time.sleep(4)
        
        
def list_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        return []
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def scan_folder_for_viruses(folder_path):
    if check_path_type(folder_path) == "file":
        return isvirus(folder_path)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            print(f"Scanning: {full_path}")

            if check_path_type(full_path) == "file":
                if isvirus(full_path):
                    print(f"Infected file found: {full_path}")
                    return True
            else:
                return scan_folder_for_viruses(full_path) # if it is a folder then check for virus inside it 
    print("No infected files found.")
    return False
print(scan_folder_for_viruses(input("input_path (use double '\\'): ")))