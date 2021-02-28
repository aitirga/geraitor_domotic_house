from geraitor_domotic_house.config import config
from geraitor_domotic_house.source.controllers import LifxController
import time


def main():
    lifx_controller = LifxController()

    for light in lifx_controller.lights.values():
        light.set_color_state(color={"brightness": 1.0}, power="on")
    lifx_controller.set_state()

    for light in lifx_controller.lights.values():
        light.set_color_state(color={"brightness": 0.25}, power="on")
    lifx_controller.set_state()

    for light in lifx_controller.lights.values():
        light.set_color_state(color={"brightness": 0.75}, power="on")
    lifx_controller.set_state()

    for light in lifx_controller.lights.values():
        light.set_color_state(color={"brightness": 0.1}, power="on")
    lifx_controller.set_state()


if __name__ == '__main__':
    main()