import secrets
import string
from fake_useragent import UserAgent
from colorama import Fore

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