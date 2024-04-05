import os
from utils import print_colored
from colorama import Fore


dir_to_remove = ["data", "archive", "temp"]
removed = []

def clean():
    for folder_path in dir_to_remove:
        if not os.path.exists(folder_path):
            continue
        try:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)

            os.rmdir(folder_path)
            removed.append(folder_path)
        except Exception as e:
            print_colored(f"Error during cleanup: {str(e)}", Fore.RED)

clean()
print_colored("Cleanup complete!", Fore.GREEN)
print_colored("Removed directories:", Fore.GREEN)
for folder in removed:
    print(folder)
