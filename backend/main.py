"""Main backend for velo supervisor 2000"""

from fastapi import FastAPI
from strava import Strava
from peewee_connector import PeeweeConnector
import argparse
import logging

# Configuration of logging - might remove this later
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"))
logging.getLogger().addHandler(CONSOLE_HANDLER)
logging.getLogger().setLevel(logging.INFO)


def read_parameters():
    """
    Function for reading variables for the script,
    for more on argparse, refer to https://zetcode.com/python/argparse/
    """
    parser = argparse.ArgumentParser(
        description="Configuration parameters")
    parser.add_argument("--oauth_file", type=str,
                        help="File with oauth user data", required=True)
    args = parser.parse_args()
    # Include file path to db as argument, also include in git-ignore

    return args





PARAMETERS = read_parameters()
strava = Strava(PARAMETERS.oauth_file)
peewee_connector = PeeweeConnector()






# Endpoints get all rides and recent rides
strava.get_rides("recent") # add separate endpoint with all as param
peewee_connector.commit_rides_bulk(strava.payload)

if len(peewee_connector.list_unique_bikes()) > 0:
    strava.get_bikes(peewee_connector.list_unique_bikes())
    peewee_connector.commit_bikes(strava.payload)


#app = FastAPI()

