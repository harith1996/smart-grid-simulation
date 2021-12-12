class UserAgent:

    """Docstring for User. """

    def __init__(self, name, home, ogoal, devices = None, schedule = None):
        # Initialize attributes
        self._name = name
        self._home = home
        self._ogoal = ogoal
        self._devices = devices or []
        self._schedule = schedule or []
    
    def add_device(self, device, schedule):
        self._devices.append(device)
        self._schedule.append(schedule)

    def use_devices(self, day, time):
        for i, s in enumerate(self._schedule):
            day_start, day_end = s[0]
            hour_start, hour_end = s[1]
            
            # Is the user using the device ?
            # If so, discharge it.
            if day >= day_start and day <= day_end \
                and time >= hour_start and time <= hour_end:

                # If it was previously plugged we unplug it.
                if self._devices[i].is_plugged():
                    self._devices[i].unplug(self._home)

                self._devices[i].discharge()
            # If not, plug it to the grid.
            elif not self._devices[i].is_plugged() and not self._devices[i].is_charged():
                # Calculate t2c by checking schedule
                t2c = (hour_start - time) % 24 # Hours till next use
                t2c += ((day_start - day) % 7) * 24 # Days till next use
                self._devices[i].plug(self._home, t2c)
    
    def get_name(self):
        return self._name
    
    def get_devices(self):
        return self._devices

    def to_string(self):
        output = f"{self._name}/{self._ogoal}\n"
        for i, d in enumerate(self._devices):
            output += f"\t↣ {d.to_string()} active at {self._schedule[i]}\n"
        return output
    
    def to_json(self):
        return {
            '_name': self._name,
            '_ogoal': self._ogoal,
            '_devices': list(map(lambda device: device.to_json(), self._devices)),
            '_schedule': self._schedule
        }