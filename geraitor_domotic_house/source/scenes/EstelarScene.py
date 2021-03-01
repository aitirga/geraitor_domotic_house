from .BaseScene import BaseScene
import random
from geraitor_domotic_house.config import config
import time
import logging

logger = logging.getLogger(__file__)


class EstelarScene(BaseScene):
    def __init__(self, starfall_probability=None,
                 starfall_light=None,
                 mean_starfall_wait=None,
                 starfall_duration=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.starfall_probability = starfall_probability if starfall_probability else config.dynamic_scenes.Estelar.starfall_probability if config.dynamic_scenes.Estelar.starfall_probability else 0.1
        self.starfall_light = starfall_light if starfall_light else config.dynamic_scenes.Estelar.starfall_light if config.dynamic_scenes.Estelar.starfall_light else {"brightness": 0.8}
        self.mean_starfall_wait = mean_starfall_wait if mean_starfall_wait else config.dynamic_scenes.Estelar.mean_starfall_wait if config.dynamic_scenes.Estelar.mean_starfall_wait else 5
        self.starfall_duration = starfall_duration if starfall_duration else config.dynamic_scenes.Estelar.starfall_duration if config.dynamic_scenes.Estelar.starfall_duration else 2.5

    def run(self):
        self.lifx_controller.set_light_objects()
        initial_colors = {light: self.lifx_controller.lights[light].get_color() for light in self.lifx_controller.lights}
        while not self.event.is_set():
            if random.random() < self.starfall_probability:
                starfall_light = random.choice(list(self.lifx_controller.lights.keys()))
                self.lifx_controller.lights[starfall_light].set_color_state(color=self.starfall_light, fast=True)
                self.lifx_controller.set_state()
                logger.info(f"Starfall fell in {starfall_light}")
                self.event.wait(self.starfall_duration * random.uniform(0.5, 1.0))
                self.lifx_controller.lights[starfall_light].set_color_state(color=initial_colors[starfall_light], fast=True)
                self.lifx_controller.set_state()
            self.event.wait(self.mean_starfall_wait * random.random())
        self.before_exit()