#!/usr/bin/env python3
"""Module for auxiliary functions"""

import json
import logging
import asyncio
import uuid
import time
import httpx

def get_current_version():
    """Function to get current program version"""
    try:
        with open('current_version.txt', 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Version unknown"

def read_config():
    """Function to read configuration file"""
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def write_config(db_path, strava_tokens):
    """Function to update configuration file"""
    try:
        updated_config = {"db_path": db_path,
                            "strava_tokens": strava_tokens}

        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(updated_config, file, indent=4)

    except OSError as error:
        # We are here now, missing return statemets

    logging.warning(f"Configuration updated. New database path is {db_path} and new strava tokens path is {strava_tokens}. Shutting down container.")

async def pull_strava_background(mode):
    """Function to pull data from Strava in the background"""
    while True:
        try:
            logging.info(f"Retrieving rides from Strava as background task. Mode set to: {mode}")
            async with httpx.AsyncClient() as client:
                pass #Remove this before deploy
                # await client.get(f"http://localhost:8000/refresh_rides/{mode}") Activate before deploying

        except Exception as error:
            logging.error(f"An error occured calling refresh rides endpoint: {error}")

        logging.info("Next pull from Strava is in two hours")
        await asyncio.sleep(7200)

def generate_unique_id():
    """Method to generates a random and unique ID"""
    unique_id_part1 = uuid.uuid4()
    unique_id_part2 = time.time()

    return f'{str(unique_id_part1)[:6]}{str(unique_id_part2)[-4:]}'

def format_component_status(status):
    """Method to display user friendly text for None values"""
    if status is not None:
        return status

    return "Not defined"
    
def format_cost(cost):
    """Method to display user friendly text for None values"""
    if cost is not None:
        return cost

    return "No estimate"

def get_component_statistics(component_list):
    """Method to summarise key data for a set of components"""
    component_statistics = {"count_installed": 0,
                            "count_not_installed": 0,
                            "count_retired": 0,
                            "count_lifetime_status_green": 0,
                            "count_lifetime_status_yellow": 0,
                            "count_lifetime_status_red": 0,
                            "count_lifetime_status_purple": 0,
                            "count_lifetime_status_grey": 0,
                            "count_service_status_green": 0,
                            "count_service_status_yellow": 0,
                            "count_service_status_red": 0,
                            "count_service_status_purple": 0,
                            "count_service_status_grey": 0,
                            "sum_cost": 0,
                            }
        
    for component in component_list:
        if component[0] == "Installed":
            component_statistics["count_installed"] += 1
        if component[0] == "Not installed":
            component_statistics["count_not_installed"] += 1
        if component[0] == "Retired":
            component_statistics["count_retired"] += 1
        if component[4] == "OK" and component[0] == "Installed":
            component_statistics["count_lifetime_status_green"] += 1
        if component[4] == "End of life approaching" and component[0] == "Installed":
            component_statistics["count_lifetime_status_yellow"] += 1
        if component[4] == "Due for replacement" and component[0] == "Installed":
            component_statistics["count_lifetime_status_red"] += 1
        if component[4] == "Lifetime exceeded" and component[0] == "Installed":
            component_statistics["count_lifetime_status_purple"] += 1
        if component[4] == "Not defined" and component[0] == "Installed":
            component_statistics["count_lifetime_status_grey"] += 1                
        if component[5] == "OK" and component[0] == "Installed":
            component_statistics["count_service_status_green"] += 1
        if component[5] == "Service approaching" and component[0] == "Installed":
            component_statistics["count_service_status_yellow"] += 1
        if component[5] == "Due for service" and component[0] == "Installed":
            component_statistics["count_service_status_red"] += 1
        if component[5] == "Service interval exceeded" and component[0] == "Installed":
            component_statistics["count_service_status_purple"] += 1
        if component[5] == "Not defined" and component[0] == "Installed":
            component_statistics["count_service_status_grey"] += 1
        if component[6] is not None and isinstance(component[6], int) and component[0] == "Installed":
                if (component[4] != "OK" and component[4] is not None) or (component[5] != "OK" and component[5] is not None):
                    component_statistics["sum_cost"] += component[6]

    if component_statistics["sum_cost"] == 0:
        component_statistics["sum_cost"] = "No estimate"
        
    return component_statistics

def calculate_percentage_reached(total, remaining):
        """Method to calculate remaining service interval or remaining lifetime as percentage"""
        if isinstance(total, int) and isinstance(remaining, int):
            return round(((total - remaining) / total) * 100, 2)
        
        return 1000
