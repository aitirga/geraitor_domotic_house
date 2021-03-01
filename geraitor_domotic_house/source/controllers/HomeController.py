from dotenv import load_dotenv, find_dotenv
from geraitor_domotic_house.source.controllers import NanoleafController, LifxController, BaseController
from geraitor_domotic_house.config import config
import os
from threading import Thread
import threading
import logging
import time
from .NanoleafController import NanoleafController

logger = logging.getLogger(__file__)


class HomeController(BaseController):
    """Controls the scene selection"""
    def __init__(self):
        super(HomeController, self).__init__()
        self.lifx_controller = LifxController()
        self.nanoleaf_controller = NanoleafController()
        self.is_running = False

    def estelar_scene(self):
        while not config.globals.stop_thread:
            self.lifx_controller.lights["Luna"].set_color_state(color={"brightness": 1.0})
            if config.globals.stop_thread:
                break
            self.lifx_controller.set_state()
            time.sleep(3)

            self.lifx_controller.lights["Luna"].set_color_state(color={"brightness": 0.1})
            if config.globals.stop_thread:
                break
            self.lifx_controller.set_state()
            time.sleep(3)

    def pastel_scene(self):
        while not config.globals.stop_thread:
            self.lifx_controller.lights["Lampara"].set_color_state(color={"brightness": 1.0})
            if config.globals.stop_thread:
                break
            self.lifx_controller.set_state()
            time.sleep(3)

            self.lifx_controller.lights["Lampara"].set_color_state(color={"brightness": 0.1})
            if config.globals.stop_thread:
                break
            self.lifx_controller.set_state()
            time.sleep(3)


    def run(self):
        """
        Returns:

        """
        logger.info("Starting to run Home Controller")
        self.is_running = True
        current_scene = self.lifx_controller.identify_scene()
        old_scene = current_scene
        change_scene = True
        while self.is_running:
            current_scene = self.lifx_controller.identify_scene()
            if current_scene != old_scene:
                config.globals.stop_thread = True
                change_scene = True
            old_scene = current_scene
            if current_scene and change_scene:
                change_scene = False
                method_to_run = f"{current_scene}_scene".lower()
                print(method_to_run)
                if hasattr(self, method_to_run):
                    logger.info(f"Customized {current_scene} scene has been set")
                    scene_thread = Thread(target=getattr(self, method_to_run))
                    scene_thread.start()
                else:
                    logger.warning(f"Scene {current_scene} is running with default settings")


