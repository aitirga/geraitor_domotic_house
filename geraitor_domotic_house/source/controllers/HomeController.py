from dotenv import load_dotenv, find_dotenv
from geraitor_domotic_house.source.controllers import NanoleafController, LifxController, BaseController
from geraitor_domotic_house.config import config
import os
from threading import Thread
import threading
import logging
import time
import ctypes
from .NanoleafController import NanoleafController
import sys
import importlib

logger = logging.getLogger(__file__)
import multiprocessing
from signal import signal, SIGTERM
from geraitor_domotic_house.source.scenes import BaseScene



class HomeController(BaseController):
    """Controls the scene selection"""
    def __init__(self):
        super(HomeController, self).__init__()
        logger.info("Setting up home controllers")
        self.lifx_controller = LifxController()
        self.nanoleaf_controller = NanoleafController()
        self.is_running = False

    def estelar_scene(self):
        self.lifx_controller.set_light_objects()
        while 1:
            self.lifx_controller.lights["Luna"].set_color_state(color={"brightness": 1.0})
            self.lifx_controller.set_state()
            time.sleep(3)

            self.lifx_controller.lights["Luna"].set_color_state(color={"brightness": 0.1})
            self.lifx_controller.set_state()
            time.sleep(3)

    def pastel_scene(self):
        self.lifx_controller.set_light_objects()
        while 1:
            self.lifx_controller.lights["Aire"].set_color_state(color={"brightness": 1.0})
            self.lifx_controller.set_state()
            time.sleep(3)

            self.lifx_controller.lights["Aire"].set_color_state(color={"brightness": 0.1})
            self.lifx_controller.set_state()
            time.sleep(3)

    def run(self):
        """
        Returns:

        """
        logger.info("Starting to run Home Controller")
        self.is_running = True
        current_scene = self.nanoleaf_controller.get_scene()
        change_scene = True
        scene_thread = BaseScene(lifx_controller=self.lifx_controller, nanoleaf_controller=self.nanoleaf_controller)
        while self.is_running:
            if current_scene != self.nanoleaf_controller.get_scene():
                scene_thread.event.set()
                change_scene = True
                current_scene = self.nanoleaf_controller.get_scene()
            if current_scene and change_scene:
                change_scene = False
                try:
                    SceneClass = getattr(importlib.import_module("geraitor_domotic_house.source.scenes"),
                                                                    f"{current_scene}Scene")
                    scene_thread: BaseScene = SceneClass(lifx_controller=self.lifx_controller,
                                              nanoleaf_controller=self.nanoleaf_controller,
                                              )
                    logger.info(f"Customized {current_scene} scene has been set")
                    scene_thread.start()
                except:
                    logger.warning(f"Default {current_scene} scene has been set")