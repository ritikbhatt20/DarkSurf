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
