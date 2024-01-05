import os
import requests
from bs4 import BeautifulSoup

def create_file_info_list(url):
    try:
        # Send a GET request
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")
            return []

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')  # Find all 'a' tags

        file_info_list = []

        # Extract torrent file links and file information
        for link in links:
            href = link.get('href')
            if href.endswith('.torrent'):
                file_url = url + href
                file_name = href.split('/')[-1]
                file_info_list.append({
                    'file_url': file_url,
                    'file_name': file_name,
                    'file_path': None  # Will be updated during download
                })

        return file_info_list

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as ex:
        print(f"Error: {ex}")
        return []

def download_torrent_files(file_info_list, folder_path):
    try:
        # Check if folder_path exists, create it if it doesn't
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")

        total_files = len(file_info_list)
        downloaded_files = 0

        # Download files if they don't exist in folder_path
        for file_info in file_info_list:
            file_name = file_info['file_name']
            file_path = os.path.join(folder_path, file_name)
            file_info['file_path'] = file_path

            if not os.path.exists(file_path):
                # File doesn't exist, download it
                print(f"Downloading {file_name}...")
                file_content = requests.get(file_info['file_url'])
                with open(file_path, 'wb') as f:
                    f.write(file_content.content)
                print(f"{file_name} downloaded successfully.")
                downloaded_files += 1
            else:
                print(f"{file_name} already exists in the specified folder.")
                downloaded_files += 1

            remaining_files = total_files - downloaded_files
            print(f"[i] [Stats] Total/Downloaded/Remaining: {total_files}/{downloaded_files}/{remaining_files}")

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except Exception as ex:
        print(f"Error: {ex}")

# Example usage:
url = "http://libgen.is/repository_torrent/"
folder_path = "./torrent_files/"   # Replace with your folder path

file_info_list = create_file_info_list(url)
download_torrent_files(file_info_list, folder_path)
