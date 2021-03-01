from .BaseController import BaseController
from geraitor_domotic_house.source.lifx_lights import A19Light, ZStripLight, BaseLight
from geraitor_domotic_house.config import config
import os
import logging
import requests
import json
logger = logging.getLogger(__file__)
from typing import Dict


class LifxController(BaseController):
    light_status_raw: dict
    lights: Dict[str, BaseLight] = {}
    def __init__(self, token=None):
        super().__init__()
        try:
            self.token = token if token else os.environ["lifx_token"]
        except:
            logger.error("Please add the Lifx Lan token into the '.env' file in your root folder")
        self.headers = {
            "Authorization": "Bearer %s" % self.token,
        }
        self.light_status = {}
        self.set_light_objects()
        logger.info("Lifx controller has been properly set-up")


    def set_light_objects(self):
        self.get_lights()
        for light in self.lights_status_raw:
            if light['product']['identifier'] == "lifx_a19":
                self.lights[light["label"]] = A19Light(token=self.token, name=light['label'], id=light['id'])
            if light['product']['identifier'] == "lifx_z2":
                self.lights[light["label"]] = ZStripLight(token=self.token, name=light['label'], id=light['id'])

    def get_lights(self):
        """
        Get light status from lifx website
        Returns:
            Dictionary containing useful light info
        """
        self.lights_status_raw = json.loads(requests.get('https://api.lifx.com/v1/lights/all', headers=self.headers).content)
        for light in self.lights_status_raw:
            self.light_status[light["label"]] = {
                'color': light["color"],
                'power': light['power'],
                'brightness': light['brightness']
            }
            if light['product']['identifier'] == 'lifx_z2':
                self.light_status[light['label']]["zones"] = light['zones']

        return self.light_status

    def set_light_color(self, color, light_name='all', filter=None, duration=1.0, power=None):
        """
        Sets the given light color on the lights
        Args:
            light_name: name of the light to which apply the constant color
            group: group or filter to apply the given color to
            duration: duration of the color change effect
            power: set power status
        """
        _color_string = ""
        for key in color:
            _color_string += f"{key}:{color[key]}"

        _data = {
            "color": _color_string,
            "duration": duration,
        }
        if power:
            _data["power"] = power

        if not filter:
            send_string = f"https://api.lifx.com/v1/lights/{light_name}/state"
        else:
            send_string = f"https://api.lifx.com/v1/lights/{light_name}:{filter}/state"

        response = requests.put(send_string, data=_data, headers=self.headers)

    def set_state(self, default_dict=None):
        _data = {}
        _data["states"] = []
        for light in self.lights.values():
            if light.state_to_be_set:
                _data["states"].append(light.state)
                light.state_to_be_set = False
        response = requests.put('https://api.lifx.com/v1/lights/states', data=json.dumps(_data), headers=self.headers)
        return response.content

    def identify_scene(self):
        self.get_lights()
        # Try to match the condition found on the config file
        found_scene = None
        for scene in config.scenes:
            lights = config.scenes[scene]
            for light in lights:
                for constrain in lights[light]:
                    if not self.light_status[light]["color"][constrain] == lights[light][constrain]:
                        self.current_scene = None
                        break
                    found_scene = scene
        if found_scene:
            self.current_scene = found_scene
            logger.debug(f"Scene {found_scene} is currently running at home")
            return self.current_scene

    # def set_scene(self):
    #
    def list_scenes(self):
        response = requests.get('https://api.lifx.com/v1/scenes', headers=self.headers)
        return json.loads(response.content)