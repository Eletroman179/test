import requests
from packaging import version
import re

CURRENT_VERSION = "1.2.0"  # Your current tool version

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

def handle_non_version_tag(tag):
    print(f"Custom Handling: Non-version tag '{tag}' found.")

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
                        return latest_release
                    else:
                        print("You are using the latest version.")
                except version.InvalidVersion as e:
                    print(f"Error: Invalid version format '{latest_version}'.")
            else:
                print(f"Non-version tag found: '{latest_version}'.")
                handle_non_version_tag(latest_version)
        else:
            print("Error: 'tag_name' not found in release info.")
    return None

# Run the update check
check_for_updates()
