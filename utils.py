import secrets
import string
from fake_useragent import UserAgent
from colorama import Fore
import csv
import os
from datetime import datetime


def print_colored(message, color=Fore.WHITE):
    print(color + message + Fore.RESET)


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random


def generate_secure_random_string(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def sanitize_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    return ''.join(char if char not in invalid_chars else '_' for char in filename)


def save_data_to_file(data, directory, filename, i2p=False):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, sanitize_filename(filename))
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(data)
    if not i2p:
        print(f"Data saved to: {filepath}")
    else:
        print_colored(f"Data saved to: {filepath}", Fore.MAGENTA)


def save_url_to_csv(filename, url, csvfile, i2p=False):
    CSV_FILE_PATH = csvfile
    with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'url', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not os.path.exists(CSV_FILE_PATH):
            writer.writeheader()
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        writer.writerow(
            {'filename': filename, 'url': url, 'timestamp': timestamp})
        if not i2p:
            print_colored(
                f"URL saved to CSV: filename={filename}, url={url}", Fore.GREEN)
        else:
            print_colored(
                f"URL saved to CSV: filename={filename}, url={url}", Fore.MAGENTA)


def save_url_to_temp_db(url, TEMP_DB_PATH='temp', i2p=False):
    os.makedirs(TEMP_DB_PATH, exist_ok=True)
    temp_db_file = os.path.join(TEMP_DB_PATH, "scraped.txt")

    # Check if the URL is already in the database
    if url in load_urls_from_temp_db():
        if not i2p:
            print_colored(
                f"URL already in temporary database: {url}", Fore.YELLOW)
        else:
            print_colored(
                f"URL already in temporary database: {url}", Fore.MAGENTA)
        return

    with open(temp_db_file, 'a', encoding='utf-8') as file:
        file.write(f"{url}\n")
    if not i2p:
        print_colored(f"URL saved to temporary database: {url}", Fore.GREEN)
    else:
        print_colored(f"URL saved to temporary database: {url}", Fore.MAGENTA)


def load_urls_from_temp_db(TEMP_DB_PATH='temp'):
    urls_set = set()
    temp_db_file_path = os.path.join(TEMP_DB_PATH, "scraped.txt")
    if os.path.exists(temp_db_file_path):
        with open(temp_db_file_path, 'r', encoding='utf-8') as file:
            urls_set.update(line.strip() for line in file if line.strip())
    return urls_set
