import requests
import json
import time
from Constants import Constants
import re
import RequestResolverDAO

def getIPRegistryDataForIp(ip):

    try:
        # Initial request going out using user's IP and the API key provided by IPRegistry
        request = requests.get("https://api.ipregistry.co/" + str(ip) + "?key=" + Constants.IPREGISTRY_KEY)

        if request.status_code != 200:
            raise Exception("IPRegistry returned a non-200 status code. Status code was: " + str(request.status_code))

        # JSON formatting, turing False to 0, True to 1, None to "None" and replacing single quotes with double quotes
        try:
            json_str = str(str(request.json()).replace("'", '"').replace("False", "0").replace("True", "1").replace("None", '"None"'))

        except Exception as e:
            raise Exception("Failed to convert JSONs Bools and Nones to appropriate equivalents. True error was: " + str(e))

        return request.json(), json_str

    except Exception as e:

        # If the request fails, raise an error inidcating that the request failed
        RequestResolverDAO.setLogsToDatabase("HTTPSError", "Error encountered while attempting to get JSON data from IPRegistry using API. Error was: " + str(e))

        # Return both possible variables as none as its clear that a faliure has occured.
        return None, None

# Checks if a url is valid and returns a boolean
def checkUrlForOk(url):

    import requests

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        RequestResolverDAO.setLogsToDatabase("HTTPSError", "Error encountered when checking for 200. Error was " + str(e))
        return False
