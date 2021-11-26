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
                self._devices[i].discharge()
            # If not, plug it to the grid.
            elif not self._devices[i].is_plugged() and not self._devices[i].is_charged():
                # Calculate t2c by checking schedule
                t2c = hour_start - time if hour_start >= time else 24.0 - time - hour_start
                t2c += (day_start - day) * 24.0 if day_start >= day else (7 - day - day_start) * 24.0
                self._devices[i].plug(time, t2c)

    def to_string(self):
        output = f"{self._name}/{self._ogoal}\n"
        for i, d in enumerate(self._devices):
            output += f"\t↣ {d.to_string()} active at {self._schedule[i]}\n"
        return output

    # Remove after testing
    def trigger_home_manager(self):
        self._home_manager.power_devices()
