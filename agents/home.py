class HomeAgent:

    """Docstring for Home. """
    
    def __init__(self):
        self._devices = dict()
        self._generators = dict()

    def power(self):
        devs = list(self._devices.values())
        for d in devs:
            d.charge(self)

    def acknowledge_device(self, device):
        is_in_devices = device._uid in self._devices
        is_in_generators = device._uid in self._generators
        
        should_add_device = not is_in_devices
        should_add_generator = device.is_generator() and not is_in_generators

        if should_add_device:
            self._devices[device._uid] = device

        if should_add_generator:
            self._generators[device._uid] = device

        return (should_add_device, should_add_generator)
    
    def disconnect_device(self, device):
        self._devices.pop(device._uid)

    def disconnect_generator(self, device):
        self._generators.pop(device._uid)
    
    def to_string(self):
        devstr = ','.join(map(str, self._devices.keys()))
        genstr = ','.join(map(str, self._generators.keys()))
        return f"devices: {{{devstr}}}; genstr: {{{genstr}}}"