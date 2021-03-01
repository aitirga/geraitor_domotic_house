from .BaseScene import BaseScene


class PastelScene(BaseScene):
    def run(self):
        self.lifx_controller.set_light_objects()
        while not self.event.is_set():
            self.lifx_controller.lights["Aire"].set_color_state(color={"brightness": 1.0}, fast=True)
            self.lifx_controller.set_state()
            self.event.wait(3)

            self.lifx_controller.lights["Aire"].set_color_state(color={"brightness": 0.1}, fast=True)
            self.lifx_controller.set_state()
            self.event.wait(3)
        self.before_exit()