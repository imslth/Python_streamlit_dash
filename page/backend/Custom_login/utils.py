
import json
from argon2 import PasswordHasher
import requests



ph = PasswordHasher() 

def check_usr_pass(username: str, password: str) -> bool:
    """
    Authenticates the username and password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_user_data = json.load(auth_json)

    for registered_user in authorized_user_data:

        if registered_user['username'] == username:
            try:
                passwd_verification_bool = ph.verify(registered_user['password'], password)
                if passwd_verification_bool == True:
                    return True
            except:
                pass
    return False


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass













