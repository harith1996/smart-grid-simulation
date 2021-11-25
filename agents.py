import json
from osbrain import Agent

class UserAgent(Agent):
    
    """Docstring for User. """

    def on_init(self):
        # Initialize attributes
        self._name = None
        self._ogoal = "cost"
        self._devices = []
        self._schedule = []
        self._home_manager = None
    
    def run_devices(self, day, time):
        for i, s in enumerate(self._schedule):
            day_start, day_end = s[0]
            hour_start, hour_end = s[1]

            # Is the user using the device ?
            # If so, discharge it.
            if day >= day_start and day <= day_end \
                and time >= hour_start and time <= hour_end:
                print(f"{self._name} uses {self._devices[i].to_string()}")
                self._devices[i].discharge()
            # If not, plug it to the grid.
            elif not self._devices[i].is_charging():
                print(f"{self._name} plugs {self._devices[i].to_string()}")
                # Calculate t2c by checking schedule
                self._devices[i].start_charge(time, time+1.0)
    
    def to_string(self):
        output = f"{self._name}/{self._ogoal}\n"
        for i, d in enumerate(self._devices):
            output += f"\t↣ {d.to_string()} active at {self._schedule[i]}\n"
        return output

class GridAgent(Agent):

    """Docstring for Grid. """

    def on_init(self):
        pass

    def to_string(self):
        pass

class HomeAgent(Agent):

    """Docstring for Home. """

    def on_init(self):
        pass

    def check_for_generator(self):
        pass

class DeviceAgent(Agent):
    
    """Docstring for Device. """

    def on_init(self):
        # Initialize attributes
        self._did = -1
        self._name = None
        self._power_limit = 1
        self._capacity = 100
        self._load_profile = 0.0001
        self._curr_charge = 0
        self._scharge = -1
        self._echarge = -1
        self._charging = False
        self._is_generator = False
    
    def start_charge(self, now, t2c):
        self._charging = True
        self._scharge = now
        self._echarge = self._scharge + t2c
    
    # By default we decrease one unit
    def discharge(self, t = 1):
        self._curr_charge = max(0, self._curr_charge - self._load_profile * t)
    
    def is_charging(self):
        return self._charging

    def to_string(self):
        return f"{self._did}/{self._name}/" \
            f"{self._power_limit}/{self._capacity}/" \
            f"{self._load_profile}/{self._curr_charge}/" \
            f"{self._scharge}/{self._echarge}"
