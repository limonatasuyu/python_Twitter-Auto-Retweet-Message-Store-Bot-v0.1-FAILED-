import requests
import random
import string
import json
import zipfile
import os


BASE_EMAIL_URL = "https://api.mail.gw"


class DictAsObject:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)


class PositiveInt:
    def __init__(self, value):
        if value != "" and (not isinstance(value, int) or value <= 0):
            raise ValueError("Value must be a positive integer")
        self.value = value


def zip_folder(input_folder, output_zip):
    # Ensure the output folder exists
    # os.makedirs(os.path.dirname(output_zip), exist_ok=True)

    # Walk through the directory and get all file paths
    file_paths = []
    for foldername, subfolders, filenames in os.walk(input_folder):
        for filename in filenames:
            file_paths.append(os.path.join(foldername, filename))

    # Create a zip file and add each file to it
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for file in file_paths:
            arcname = os.path.relpath(file, input_folder)
            zipf.write(file, arcname=arcname)


def generate_password(length=22):
    letters_upper = string.ascii_uppercase
    letters_lower = string.ascii_lowercase
    digits = string.digits
    special_characters = "!@#$%^&*()_+=-[]{}|;:'\"<>,.?/\\"

    all_characters = letters_upper + letters_lower + digits + special_characters

    password = ''.join(random.choice(all_characters) for _ in range(length))

    return password


def generate_random_string(length=10):
    letters_lower = string.ascii_lowercase
    digits = string.digits
    special_characters = "_-."

    all_characters = letters_lower + digits + special_characters

    first_char = random.choice(letters_lower)
    rest_of_string = ''.join(random.choice(all_characters) for _ in range(length - 1))

    random_string = first_char + rest_of_string

    return random_string


def get_domain():
    url = BASE_EMAIL_URL + '/domains'
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        return []

    data = r.json()
    domains = []

    for i in data["hydra:member"]:
        domains.append(i["domain"])

    return random.choice(domains)


def generate_email():
    domain = get_domain()
    local = generate_random_string()

    email_address = local + '@' + domain

    return email_address


def create_account():
    email_address = generate_email()
    password = generate_password()

    url = BASE_EMAIL_URL + '/accounts'
    payload = {"address": email_address, "password": password}
    headers = {"Content-Type": "application/json"}

    r = requests.post(url, json=payload, headers=headers)
    responseData = r.json()
    if r.status_code != 200 and r.status_code != 201:
        raise Exception(f"Error While Creating Email Account: {r.status_code} \n {responseData}")
        return

    data = responseData
    data["password"] = password

    return data


def get_token(email_address, password):
    url = BASE_EMAIL_URL + '/token'
    payload = {"address": email_address, "password": password}
    headers = {"Content-Type": "application/json"}

    r = requests.post(url, json=payload, headers=headers)
    responseData = r.json()
    if r.status_code != 200:
        raise Exception(f"Error While Getting The Token: {r.status_code} \n {responseData}")
        return

    token = responseData["token"]
    return token


def delete_all_messages(email_address, password):

    messages = get_messages(email_address, password)
    token = get_token(email_address, password)

    for message in messages["hydra:member"]:
        message_id = message["id"]

        url = BASE_EMAIL_URL + '/messages/' + message_id
        headers = {"Authorization": f"Bearer {token}"}

        try:
            r = requests.delete(url, headers=headers)
            if r.status_code != 204:
                print("Error while deleting a message")
                print(f"Unexpected status code from delete request: {r.status_code}")
            else:
                responseData = r.json()
                print(f"message deleted successfully: {responseData}")
        except Exception as e:
            print(f"Error while deleting a message: {e}")


def get_messages(email_address, password):
    token = get_token(email_address, password)

    url = BASE_EMAIL_URL + '/messages'
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)
    responseData = r.json()

    return responseData


def get_message(email_address, password, downloadUrl):
    token = get_token(email_address, password)

    if token is None:
        print("Error: Unable to obtain a valid token.")
        return None

    url = BASE_EMAIL_URL + downloadUrl

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(f"Error: Request failed with status code {r.status_code}")
        return None

    try:
        responseData = r.json()
    except json.JSONDecodeError:
        print("Warning: Unable to parse response as JSON. Treating as plain text.")
        responseData = r.text

    return responseData
