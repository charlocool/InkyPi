import logging
import os
from datetime import datetime, timezone

import pytz
import requests
from plugins.base_plugin.base_plugin import BasePlugin

logger = logging.getLogger(__name__)

F1_CONSTRUCTOR_STANDINGS_URL = "https://api.jolpi.ca/ergast/f1/current/constructorstandings/"
F1_DRIVER_STANDINGS_URL = "https://api.jolpi.ca/ergast/f1/current/driverstandings/"


class F1Standings(BasePlugin):
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        return template_params

    def get_constructor_standings_data(self):
        url = F1_CONSTRUCTOR_STANDINGS_URL
        response = requests.get(url)
        if not 200 <= response.status_code < 300:
            logging.error(f"Failed to retrieve constructor standings data: {response.content}")
            raise RuntimeError("Failed to retrieve constructor standings data.")
        return response.json()

    def parse_constructor_standings_data(self, constructor_standings_data):
        standing_list = constructor_standings_data['MRData']['StandingsTable']['StandingsLists'][0][
            'ConstructorStandings']
        standings = {}
        for standing in standing_list:
            standings[standing['Constructor']['constructorId']] = {
                'position': standing['position'],
                'points': standing['points'],
                'wins': standing['wins']
            }
        return standings

    def get_driver_standings_data(self):
        url = F1_DRIVER_STANDINGS_URL
        response = requests.get(url)
        if not 200 <= response.status_code < 300:
            logging.error(f"Failed to retrieve driver standings data: {response.content}")
            raise RuntimeError("Failed to retrieve driver standings data.")
        return response.json()

    def parse_driver_standings_data(self, driver_standings_data):
        standing_list = driver_standings_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        standings = {}
        for standing in standing_list:
            standings[standing['Driver']['driverId']] = {
                'first_name': standing['Driver']['givenName'],
                'last_name': standing['Driver']['familyName'],
                'number': standing['Driver']['permanentNumber'],
                'position': standing.get('position', 'N/A'),
                'points': standing['points'],
                'wins': standing['wins']
            }
        return standings

    def parse_driver_leader(self, driver_standings_data) -> dict:
        current_leader_name = list(driver_standings_data.keys())[0]
        data = {
            "current_leader_icon": self.get_plugin_dir(f'icons/drivers/{current_leader_name}.png'),
            "current_points": driver_standings_data[current_leader_name]['points']
        }
        return data

    def generate_image(self, settings, device_config):
        driver_standings_data = self.parse_driver_standings_data(self.get_driver_standings_data())

        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        template_params = self.parse_driver_leader(driver_standings_data)

        image = self.render_image(
            dimensions, 'f1_standings.html', 'f1_standings.css', template_params
        )
        return image
