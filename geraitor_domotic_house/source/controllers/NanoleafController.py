from nanoleafapi import Nanoleaf
from nanoleafapi.discovery import discover_devices
from .BaseController import BaseController
import os
import logging

logger = logging.getLogger(__file__)


class NanoleafController(BaseController):
    """
    This class controls the Nanoleaf lights
    """
    def __init__(self):
        super(NanoleafController, self).__init__()
        self.device = Nanoleaf(ip="192.168.1.155", auth_token=os.environ["nanoleaf_token"])
        logger.info("Nanoleaf controller has been properly set-up")

    def get_scene(self):
        return self.device.get_current_effect()