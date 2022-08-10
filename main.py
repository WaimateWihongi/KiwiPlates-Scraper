import requests
import itertools
import colorama
import time
from string import ascii_uppercase, digits

MAX_CHARS = 6
CHARS = list(ascii_uppercase + digits)

def get_plate(plate):
    """
    Get the number plate data from the API.
    @param plate: The number plate to search for.
    """
    url = "https://api.kiwiplates.nz/api/combination/%s/?vehicleTypeId=1"
    resp = requests.get(url % plate)
    if resp.status_code == 200:
        return resp.json()

def generate_plates(repeat):
    """
    Generate a number plate from the given characters.
    """
    yield from itertools.product(CHARS, repeat=repeat)

if __name__ == "__main__":
    # Colorama stuff
    colorama.init()

    for number in range(MAX_CHARS):
        for x in generate_plates(number):
            plate = ''.join(x)
            resp = get_plate(plate)
            if resp:
                if resp["Data"]["Available"]:
                    print(plate + "\t" + colorama.Fore.LIGHTGREEN_EX + "[Available]" + colorama.Fore.RESET)
                    with open("plates.txt", "a+") as f:
                        f.write(plate + "\n")
                else:
                    print(plate + "\t" + colorama.Fore.LIGHTRED_EX + "[Not Available]" + colorama.Fore.RESET)
            time.sleep(0.5)
