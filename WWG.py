
#© Joseph Toscano (2024)"
# This is an installation and update program for wizards with guns
# While isnide of the same directory as the .py file use this command
# python -m nuitka --onefile --windows-icon-from-ico=ico.png .\WWG.py


import os
import shutil
import urllib.request
import urllib.error
import subprocess
import time
import ctypes


MAIN_URL = "https://www.wizardswithguns.com"
VERSION_URL = f"{MAIN_URL}/version"
DOWNLOAD_URL_TEMPLATE = f"{MAIN_URL}/download/{{}}.zip"
INSTALL_DIR = os.path.join(os.getenv('APPDATA'), 'wizards-with-guns')

ascii_art = [
"░  ░░░░  ░░        ░░        ░░░      ░░░       ░░░       ░░░░      ░░░░░░░░░  ░░░░  ░░░░░░░░░      ░░░  ░░░░  ░░   ░░░  ░░░      ░░",
"▒  ▒  ▒  ▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒  ▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒  ▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒    ▒▒  ▒▒  ▒▒▒▒▒▒▒",
"▓        ▓▓▓▓▓  ▓▓▓▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓  ▓▓       ▓▓▓  ▓▓▓▓  ▓▓▓      ▓▓▓▓▓▓▓▓▓        ▓▓▓▓▓▓▓▓  ▓▓▓   ▓▓  ▓▓▓▓  ▓▓  ▓  ▓  ▓▓▓      ▓▓",
"█   ██   █████  ██████  ███████        ██  ███  ███  ████  ████████  ████████   ██   ████████  ████  ██  ████  ██  ██    ████████  █",
"█  ████  ██        ██        ██  ████  ██  ████  ██       ████      █████████  ████  █████████      ████      ███  ███   ███      ██",
    "© Joseph Toscano (2024)"
]

def main():
    try:
        os.system('color 2')
        print_art_line_by_line(ascii_art)
        latest_version = get_latest_version()

        if os.path.exists(INSTALL_DIR):
            current_version = get_current_version()
            if current_version != latest_version:
                print(f"Updating from version {current_version} to {latest_version}...")
                download_and_install(latest_version)
            else:
                print(f"You already have the latest version: {current_version}")
        else:
            print("Installing the latest version...")
            download_and_install(latest_version)

        launch_game()

    except urllib.error.URLError:
        if ask_launch_game():
            launch_game()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            display_error_message("404 Error: The requested URL was not found on the server.")
        else:
            display_error_message(f"HTTP Error: {e.code}")
    except Exception as e:
        display_error_message(f"An unexpected error occurred: {str(e)}")

def print_art_line_by_line(art):
    for line in art:
        for char in line:
            print(char, end='', flush=True)
            time.sleep(0.001)  # Adjust sleep time for different speeds
        print()  # Move to next line

def get_latest_version():
    with urllib.request.urlopen(VERSION_URL) as response:
        html = response.read().decode('utf-8')
        latest_version = extract_version(html)
        return latest_version

def extract_version(html):
    for line in html.splitlines():
        if "Latest Unstable Version" in line:
            return line.split(":")[1].strip()
    raise ValueError("Version information not found in HTML response")

def get_current_version():
    version_file = os.path.join(INSTALL_DIR, 'ver.txt')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            return f.read().strip()
    return None

def download_and_install(version):
    url = DOWNLOAD_URL_TEMPLATE.format(version)
    if not os.path.exists(INSTALL_DIR):
        os.makedirs(INSTALL_DIR)  # Ensure the installation directory exists
    zip_file = os.path.join(INSTALL_DIR, f"{version}.zip")

    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, zip_file)

    print("Extracting...")
    shutil.unpack_archive(zip_file, INSTALL_DIR)

    os.remove(zip_file)  # Clean up the zip file

    # Write the current version number to 'ver.txt'
    version_file = os.path.join(INSTALL_DIR, 'ver.txt')
    with open(version_file, 'w') as f:
        f.write(version)

    print(f"Version {version} installed successfully.")

def launch_game():
    exe_path = os.path.join(INSTALL_DIR, 'wizards-with-guns.exe')
    if os.path.exists(exe_path):
        print("Launching the game...")
        subprocess.Popen([exe_path], cwd=INSTALL_DIR)  # Use Popen to not wait for the process

def display_error_message(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Error", 0x10)  # 0x10 is the MB_ICONERROR flag

def ask_launch_game():
    MB_YESNO = 0x04
    IDYES = 6
    result = ctypes.windll.user32.MessageBoxW(0, "WizardsWithGuns.com is not responding. Your internet connection may be experiencing issues. Would you like to launch the game anyway?", "Error", MB_YESNO | 0x10)
    return result == IDYES

if __name__ == "__main__":
    main()
