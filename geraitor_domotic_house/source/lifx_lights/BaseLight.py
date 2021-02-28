from geraitor_domotic_house.source.controllers import LifxController


class BaseLight:
    """
    This class contains basic methods and functionalities to control a Lifx light
    """
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": "Bearer %s" % self.token,
        }

    def get_color(self):
        """
        Gets the color of the light
        Returns:

        """