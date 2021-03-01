from .BaseScene import BaseScene


class EstelarScene(BaseScene):
    def run(self):
        self.lifx_controller.set_light_objects()
        print("running")
        while not self.event.is_set():
            self.lifx_controller.lights["Luna"].set_color_state(color={"brightness": 1.0})
            self.lifx_controller.set_state()
            self.event.wait(3)

            self.lifx_controller.lights["Luna"].set_color_state(color={"brightness": 0.1})
            self.lifx_controller.set_state()
            self.event.wait(3)
        self.before_exit()