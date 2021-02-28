from dotenv import load_dotenv, find_dotenv
import os


class BaseController:
    def __init__(self, token=None):
        load_dotenv()

    def get_color(self):
        """
        Gets the color of the light
        Returns: dictionary containing the color of the light
        """

