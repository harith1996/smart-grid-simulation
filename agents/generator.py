import random
from agents.device import DeviceAgent


class GeneratorAgent(DeviceAgent):

    def __init__(self, did, owner, init_charge):
        super().__init__(did, owner, init_charge)
        self._peak_load = 0
        self._current_load = 0
        self._load_limit = 5000 + random.random() * 1000

    def get_current_price(self, day=0, time=0):
        """Returns price of consuming power from this generator

        Returns:
            [type]: [description]
        """
        return 0

    def connect_power(self, power_limit):
        """Called by a device when charging.

        Args:
            power_limit (int): Max power drawn by the device

        Returns:
            Boolean: True if device is allowed to connect
        """
        self._current_load += power_limit
        if(self._peak_load < self._current_load):
            self._peak_load = self._current_load
        return True

    def disconnect_power(self, power_limit):
        """Called by a device when disconnecting from grid.

        Args:
            power_limit (int): Max power drawn by the device

        Returns:
            Boolean: True if device can safely disconnect
        """
        self._current_load -= power_limit
        return True
