import json
from osbrain import Agent

class UserAgent(Agent):
    
    """Docstring for User. """

    def on_init(self):
        # Initialize attributes
        self._name = None
        self._ogoal = "cost"
        self._devices = []

    def to_string(self):
        output = f"{self._name}/{self._ogoal}\n"
        for d in self._devices:
            output += f"\t↣ {d.to_string()}\n"
        return output

class GridAgent(Agent):

    """Docstring for Grid. """

    def on_init(self):
        pass

    def to_string(self):
        pass

class DeviceAgent(Agent):
    
    """Docstring for Device. """

    def on_init(self):
        # Initialize attributes
        self._did = -1
        self._name = None
        self._power_limit = 1
        self._capacity = 100
        self._load_profile = {'x': 1.0, 'y': 1.0}
        self._curr_charge = 0
        self._scharge = -1
        self._echarge = -1

    def start_charge(self, now, t2c):
        self._scharge = now
        self._echarge = self.scharge + t2c

    def to_string(self):
        return f"{self._did}/{self._name}/" \
            f"{self._power_limit}/{self._capacity}/" \
            f"{self._load_profile}/{self._curr_charge}/" \
            f"{self._scharge}/{self._echarge}"
