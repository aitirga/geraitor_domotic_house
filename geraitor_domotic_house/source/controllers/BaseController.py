from dotenv import load_dotenv, find_dotenv
import os


class BaseController:
    def __init__(self, token=None):
        load_dotenv()

    def identify_scene(self):
        """
        This method identifies the scene that is running in the house
        Returns: string identifier of the running scene
        """
        light_status = self.get_lights()

    def get_lights(self):
        pass
