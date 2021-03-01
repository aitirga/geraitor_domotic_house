from geraitor_domotic_house.config import config
from geraitor_domotic_house.source.controllers import LifxController, HomeController
import time
from nanoleafapi import discovery, Nanoleaf


def main():
    home_controller = HomeController()

    home_controller.run()


if __name__ == '__main__':
    main()