import requests
from packaging import version
import re
import os

CURRENT_VERSION = "1.2.0"  # Your current tool version
DOWNLOAD_DIR = "downloads"  # Directory where you want to save the downloaded file

def get_latest_release_info(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print("No releases found for this repository.")
    else:
        print(f"Error fetching release info: {response.status_code} - {response.json()}")
    return None

def is_valid_version(tag):
    pattern = re.compile(r'^v?\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$')
    return pattern.match(tag) is not None

def download_file(url, local_filename):
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(local_filename), exist_ok=True)
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded to {local_filename}")
    else:
        print(f"Failed to download file: {response.status_code} - {response.text}")

def check_for_updates():
    repo_owner = "Eletroman179"
    repo_name = "test"

    latest_release = get_latest_release_info(repo_owner, repo_name)
    if latest_release:
        if 'tag_name' in latest_release:
            latest_version = latest_release["tag_name"]
            print(f"Latest version: {latest_version}")
            if is_valid_version(latest_version):
                try:
                    parsed_version = version.parse(latest_version.lstrip('v'))
                    if parsed_version > version.parse(CURRENT_VERSION):
                        print(f"Update available: {latest_version}")
                        assets = latest_release.get('assets', [])
                        if assets:
                            # Assuming the first asset is the one you want to download
                            asset = assets[0]
                            download_url = asset['browser_download_url']
                            filename = os.path.join(DOWNLOAD_DIR, asset['name'])
                            download_file(download_url, filename)
                        else:
                            print("No assets available for download.")
                    else:
                        print("You are using the latest version.")
                except version.InvalidVersion as e:
                    print(f"Error: Invalid version format '{latest_version}'.")
            else:
                print(f"Non-version tag found: '{latest_version}'.")
        else:
            print("Error: 'tag_name' not found in release info.")
    return None

# Run the update check
check_for_updates()
