from geraitor_domotic_house.source.controllers import LifxController
import json
import requests

class BaseLight:
    """
    This class contains basic methods and functionalities to control a Lifx light
    """
    def __init__(self, token, name, id):
        self.token = token
        self.headers = {
            "Authorization": "Bearer %s" % self.token,
        }
        self.name = name
        self.id = id
        self.state = {}
        self.state_to_be_set = False

    def get_status(self):
        self.light_status = json.loads(
            requests.get(f'https://api.lifx.com/v1/lights/{self.id}', headers=self.headers).content)[0]

    def get_color(self):
        """
        Gets the color of the light
        Returns:
        """
        self.get_status()
        return self.light_status['color']

    def set_color(self, color, duration=1.0, power=None):
        """
        Sets the specified color into the light
        Args:
            color: color to be set
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

        send_string = f"https://api.lifx.com/v1/lights/{self.id}/state"

        response = requests.put(send_string, data=_data, headers=self.headers)

    def set_color_state(self, color, brightness=None, power="on", time=None, **kwargs):
        """
        Sets a given color state into a light
        Args:
            color: dictionary containing color options
            brightness: float value between [0.0, 1.0] specifying the brightness
            power: Switch the
            time: Duration of the effect
            **kwargs: Other arguments
        """
        self.state["selector"] = f"id:{self.id}"
        for kwarg in kwargs:
            self.state[kwarg] = kwargs[kwarg]
        if color:
            color_string = ""
            for key in color:
                if not color[key]:
                    color_string += f"{key} "
                    continue
                color_string += f"{key}:{color[key]} "
        self.state["color"] = color_string[:-1]
        self.state["power"] = power
        self.state_to_be_set = True
