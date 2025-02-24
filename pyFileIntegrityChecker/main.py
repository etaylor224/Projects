import json
import os
from tkinter import filedialog
from hashlib import sha256


def does_hash_file_exist() -> bool:
    path_exists = False
    if os.path.exists(f"{os.getcwd()}/hashes.json"):
        path_exists = True
    return path_exists

def get_files_in_dir():
    working_dir = filedialog.askdirectory()
    return [f"{working_dir}/{file}" for file in os.listdir(working_dir)]

def create_hash(file):
    hasher = sha256()
    with open(file, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def load_prev_hashes():
    with open("hashes.json") as j:
        return json.load(j)

def comp_hashes(curr_hash, old_hash):

    print("Comparing hashes...")
    for file in curr_hash:
        if file in old_hash:
            if old_hash[file] != curr_hash[file]:
                print(f"{file} was modified!")

        elif file not in old_hash:
            print(f"{file} is new, adding to hashes")

    for file in old_hash:
        if file not in curr_hash:
            print(f"{file} was previously deleted")

def update_file(hash):
    with open('hashes.json', 'w') as j:
        json.dump(hash, j, indent=4)
        return

def allow_update():
    choice = input("Would you like to update the hash file? Y/N: ")
    if choice.lower() == 'y':
        return True
    else:
        return False

def main():

    if not does_hash_file_exist():
        print("Hash file does not exist....")
        print("Creating Hash File")

        with open('hashes.json', "w") as j:
            json.dump({}, j)

        print("Hash File created...")

    files = get_files_in_dir()
    curr_hashed = dict()
    print("Hashing files in directory...")

    #TODO check for sub directories and hash

    for file in files:
        hashed = create_hash(file)
        curr_hashed[file] = hashed
    print("Directory hashed...")

    old_hash = load_prev_hashes()
    comp_hashes(curr_hashed, old_hash)
    if allow_update():
        print("Updating Hash File")
        update_file(curr_hashed)
    else:
        print("Hash File not updated")
    return

if __name__ == "__main__":
    print("Starting File Integrity Checker")
    main()
