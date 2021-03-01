import threading
from geraitor_domotic_house.source.controllers import NanoleafController, LifxController

class BaseScene(threading.Thread):
    def __init__(self, lifx_controller, nanoleaf_controller):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.lifx_controller: LifxController = lifx_controller
        self.nanoleaf_controller: NanoleafController = nanoleaf_controller

    def run(self):
        while not self.event.is_set():
            pass
        self.before_exit()

    def before_exit(self):
        get_current_scene = self.nanoleaf_controller.get_scene()
        for scene in self.lifx_controller.list_scenes():
            print(scene["name"])

