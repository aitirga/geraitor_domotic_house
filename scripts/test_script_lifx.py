from geraitor_domotic_house.config import config
from geraitor_domotic_house.source.controllers import LifxController

def main():
    lifx_controller = LifxController()
    lifx_controller.set_light_color(color={"brightness":1.0})


if __name__ == '__main__':
    main()