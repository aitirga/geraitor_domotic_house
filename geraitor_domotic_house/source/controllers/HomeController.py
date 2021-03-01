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

logger = logging.getLogger(__file__)
import multiprocessing
from signal import signal, SIGTERM
from geraitor_domotic_house.source.scenes import EstelarScene, PastelScene, BaseScene



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
                if current_scene == "Estelar":
                    logger.info(f"Customized {current_scene} scene has been set")
                    scene_thread = EstelarScene(lifx_controller=self.lifx_controller, nanoleaf_controller=self.nanoleaf_controller)
                    scene_thread.start()
                elif current_scene == "Pastel":
                    logger.info(f"Customized {current_scene} scene has been set")
                    scene_thread = PastelScene(lifx_controller=self.lifx_controller, nanoleaf_controller=self.nanoleaf_controller)
                    scene_thread.start()
                else:
                    logger.warning(f"Scene {current_scene} is running with default settings")

                # method_to_run = f"{current_scene}_scene".lower()
                # if hasattr(self, method_to_run):
                #     logger.info(f"Customized {current_scene} scene has been set")
                #     config.globals.stop_thread = False
                #     # scene_process = threading.Thread(target=EstelarScene().run, args=(self.lifx_controller,))
                #     # scene_process.start()
                #     if
                #     scene_thread = EstelarScene(lifx_controller=self.lifx_controller)
                #     scene_thread.start()
                # else:
                #     logger.warning(f"Scene {current_scene} is running with default settings")




# class EstelarScene(threading.Thread):
#     def __init__(self, lifx_controller):
#         threading.Thread.__init__(self)
#         self.event = threading.Event()
#         self.lifx_controller = lifx_controller
#
#     def run(self):
#         self.lifx_controller.set_light_objects()
#         print("running")
#         while not self.event.is_set():
#             self.lifx_controller.lights["Luna"].set_color_state(color={"brightness": 1.0})
#             self.lifx_controller.set_state()
#             self.event.wait(3)
#
#             self.lifx_controller.lights["Luna"].set_color_state(color={"brightness": 0.1})
#             self.lifx_controller.set_state()
#             self.event.wait(3)
#         print("stopping")
#
#     def before_exit(self):
#         print("Before exit")
#         sys.exit()
#
#
# class PastelScene(threading.Thread):
#     def __init__(self, lifx_controller):
#         threading.Thread.__init__(self)
#         self.event = threading.Event()
#         self.lifx_controller = lifx_controller
#
#     def run(self):
#         self.lifx_controller.set_light_objects()
#         print("running")
#         while not self.event.is_set():
#             self.lifx_controller.lights["Lampara"].set_color_state(color={"brightness": 1.0})
#             self.lifx_controller.set_state()
#             self.event.wait(3)
#
#             self.lifx_controller.lights["Lampara"].set_color_state(color={"brightness": 0.1})
#             self.lifx_controller.set_state()
#             self.event.wait(3)
#         self.before_exit()
#
#     def before_exit(self):
#         sys.exit()