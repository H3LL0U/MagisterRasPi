import os
from pathlib import Path
PATH_TO_CREDENTIALS = "./credentials/credentials.txt"

CREDENTIALS_FOLDER_PATH = "./credentials"


def create_credentials_storage():
    if not os.path.exists(PATH_TO_CREDENTIALS):

        Path(CREDENTIALS_FOLDER_PATH).mkdir(parents=True, exist_ok=True)
        with open(PATH_TO_CREDENTIALS,"w") as path:
            pass

def check_for_saved_credentials():
    create_credentials_storage()
    with open(PATH_TO_CREDENTIALS,"r") as saved_credentials:
        saved_credentials = saved_credentials.read()
        if "PASSWORD=" in saved_credentials and "SCHOOL_NAME=" in saved_credentials and "USERNAME=" in saved_credentials:
            return True
        return False
def clear_saved_credentials():
    with open(PATH_TO_CREDENTIALS,"w") as saved_credentials:
        pass
        
def get_saved_credentials():
    with open(PATH_TO_CREDENTIALS,"r") as saved_credentials:
        content = saved_credentials.read()
        split_content = content.split("\n")
        for credential in split_content:
            if credential.startswith("SCHOOL_NAME="):
                school = credential.replace("SCHOOL_NAME=","")
            if credential.startswith("USERNAME="):
                username = credential.replace("USERNAME=","")
            if credential.startswith("PASSWORD="):
                password = credential.replace("PASSWORD=", "")
    
    return (school,username,password)

def save_new_credentials(school_name,username,password):
    clear_saved_credentials()
    with open(PATH_TO_CREDENTIALS,"w") as credentials:
        lines = [
            f"SCHOOL_NAME={school_name}\n",
            f"USERNAME={username}\n",
            f"PASSWORD={password}\n"
        ]
        credentials.writelines(lines)
