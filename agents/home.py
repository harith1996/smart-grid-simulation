import random
from typing import List
from agents.device import DeviceAgent
from agents.generator import GeneratorAgent
from utils import color_mapper


class HomeAgent:

    """Docstring for Home. """
    
    def __init__(self):
        self._owner = None
        self._devices = dict()
        self._generators = dict()
        self._bill = 0
        self._price_limit = 19e-6 + (random.random() * 5e-6)

    def power(self, power_source, day, t):
        devs = list(self._devices.values())
        gens = list(self._generators.values())
        owner = self.get_owner().get_name()
        for d in devs:
            if(d.is_plugged()):
                curr_price = power_source.get_current_price(day, t)
                if(curr_price < self._price_limit):
                    if(not d.is_charging()):
                        self._power_draw += float(d.charge(self, power_source))
                else: 
                    print(f"[⚠️] Current price {float(curr_price)} is too high for household owned by {owner}!!!")
                    if(len(gens) > 0):
                        # charge from generator instead
                        print(f"[⚡] {owner} is now charging {d.get_name()} from {gens[0].get_name()} !")
                        self._power_draw += float(d.charge(self, gens[0]))
                        
                        # time.sleep(0.5)

    def reset_power_draw(self):
        self._power_draw = 0.0
    
    def get_owner(self):
        return self._owner
    
    def set_owner(self, owner):
        self._owner = owner

    def acknowledge_device(self, device:DeviceAgent):
        is_in_devices = device._uid in self._devices
        is_in_generators = device._uid in self._generators
        
        should_add_device = not is_in_devices
        should_add_generator = device.is_generator() and not is_in_generators

        if should_add_device:
            self._devices[device._uid] = device

        if should_add_generator:
            self._generators[device._uid] = GeneratorAgent(device._did, device._owner, 0)

        return (should_add_device, should_add_generator)
    
    def disconnect_device(self, device):
        self._devices.pop(device._uid)

    def disconnect_generator(self, device):
        self._generators.pop(device._uid)
    
    def get_charging_devices(self):
        charging : List[DeviceAgent] = []
        for device in list(self._devices.values()):
            if(device._is_charging):
                charging.append(device)
        return charging

    def get_power_draw(self, power_source):
        pw_drw = 0
        for device in self.get_charging_devices():
            if(type(device._power_source) == type(power_source)):
                pw_drw += int(device.get_power_limit())
        return pw_drw
    
    def increment_bill(self, increment):
        self._bill+=increment
    
    def get_current_bill(self):
        return self._bill
        
    def to_graph(self, contidx):
        nodes, links, unlinks = [], [], []
        homeidx = contidx
        # Add home manager (and link it later in GridAgent)
        nodes.append({'id': homeidx, 'label': self._owner.get_name(), 'image': 'house-user-solid.png', 'shape': 'image'})
        contidx += 1
        # Add devices and link them to home manager
        for d in self._owner.get_devices():
            charge = d.get_charge()
            nodes.append({'charge': charge, 'id': contidx, 'title': f"Charge: {round(charge * 100, 2)}%", 'color': color_mapper(charge)})
            # Change value to something meaningful
            if d.is_connected():
                links.append({'id': contidx, 'from': contidx, 'to': homeidx})
            else:
                unlinks.append(contidx)
            # Increase counter (needed for Vis JS)
            contidx += 1

        return nodes, links, unlinks, contidx

    def to_string(self):
        devstr = ','.join(map(str, self._devices.keys()))
        genstr = ','.join(map(str, self._generators.keys()))
        return f"devices: {{{devstr}}}; genstr: {{{genstr}}}"
    
    def toJSON(self):
        return {
            '_owner': self._owner.toJSON(),
            '_price_limit': self._price_limit
        }
