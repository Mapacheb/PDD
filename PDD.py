import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import platform
import signal
import webbrowser
from colorama import Fore

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def signal_handler(sig, frame):
    clear_screen()
    print("Ok, byeee :)")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

clear_screen()

if not os.path.exists('ai.p2p'):
    webbrowser.open('https://github.com/Mapacheb')
    with open('ai.p2p', 'w') as f:
        f.write('true')

print(Fore.BLUE + '''
|---------------------------------------------------------------------------------|
 Changelog v1.1:                                                                 
 Subdirectories            8888888b.  8888888b.  8888888b.                       
 New Formats:              888   Y88b 888  "Y88b 888  "Y88b                      
  • MP4, WMV, ZIP,         888    888 888    888 888    888                      
    JPG, PDF, SH           888   d88P 888    888 888    888                      
    BAT+                   8888888P"  888    888 888    888                      
 Optimized Code            888        888    888 888    888                      
                           888        888  .d88P 888  .d88P                      
                           888        8888888P"  8888888P"                       
                           Python     Directory  Downloader                      
                                                                                 
''' + Fore.WHITE + '''                      [PDD - Dedicated to elhacker.info/Cursos/]                 
                                 Creator: mapacheb                               
'''+ Fore.CYAN +'''                                                                    Version 1.1 
''' + Fore.BLUE + ''' 
|---------------------------------------------------------------------------------|
''')

base_url = input("[PDD]: ")

def download_file(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, url.split("/")[-1])
    
    if os.path.exists(filename):
        print(f'[PDD]: {filename} Already Exist, Skipping download...')
        return

    response = requests.head(url)
    total_size = int(response.headers.get('content-length', 0))

    with requests.get(url, stream=True) as r, open(filename, 'wb') as f:
        downloaded_size = 0
        chunk_size = 8192
        total_chunks = total_size // chunk_size + (total_size % chunk_size > 0)

        print(Fore.GREEN + f"Downloading: {filename.split('/')[-1]}")
        for _ in range(total_chunks):
            chunk = r.raw.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            downloaded_size += len(chunk)

            percent = (downloaded_size / total_size) * 100
            bar_length = 10
            block = int(round(bar_length * percent / 100))
            progress_bar = f"[{'=' * block}{' ' * (bar_length - block)}] {percent:.2f}%"
            print(Fore.YELLOW + f"\r{progress_bar}", end='')

        print()

    print(Fore.GREEN + f'Downloaded :)')
    clear_screen()

def process_directory(url, parent_folder):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(Fore.RED + f"[PDD]: Error getting {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    decoded_folder = unquote(url.split("/")[-2])
    folder = os.path.join(parent_folder, decoded_folder)

    if not os.path.exists(folder):
        os.makedirs(folder)

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)
            if link.find_previous('img', alt="[Directorio]"):
                process_directory(full_url, folder)
            elif href.endswith(('.mp4', '.wmv', '.pdf', '.zip', '.bat', '.sh', '.sql', 
                                '.plb',  '.jpg', '.gif', '.png', '.doc', '.mht')):
                download_file(full_url, folder)

    print(Fore.GREEN + f'Finished processing directory: {folder}')


process_directory(base_url , '.')
print(Fore.GREEN + 'All directories processed successfully.')