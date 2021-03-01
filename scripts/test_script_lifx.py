from geraitor_domotic_house.config import config
from geraitor_domotic_house.source.controllers import LifxController, HomeController
import time
from nanoleafapi import discovery, Nanoleaf

def estelar_scene():
    pass


def main():

    test_nanoleaf = Nanoleaf(ip="192.168.1.155")
    print(test_nanoleaf.create_auth_token())

    # home_controller = HomeController()
    # home_controller.run()


    # lifx_controller = LifxController()
    #
    # # while 1:
    # #     lifx_controller.identify_scene()
    #
    # lifx_controller.lights["Luna"].set_color_state(color={"red": None, "saturation": 0.1, "brightness": 1.0}, duration=3, fast=True)
    # lifx_controller.set_state()


if __name__ == '__main__':
    main()