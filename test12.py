CURRENT_VERSION = "1.0.0"  # Your current tool version

def check_for_updates():
    repo_owner = "Eletroman179"
    repo_name = "test"

    latest_release = get_latest_release_info(repo_owner, repo_name)
    if latest_release:
        latest_version = latest_release["tag_name"]
        if latest_version > CURRENT_VERSION:
            print(f"Update available: {latest_version}")
            return latest_release
        else:
            print("You are using the latest version.")
    return None
import requests

def get_latest_release_info(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch release information.")
        return None

check_for_updates()