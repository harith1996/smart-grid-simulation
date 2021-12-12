from functools import reduce
import json
from typing import List
from agents.device import DeviceAgent
from agents.generator import GeneratorAgent
from utils import color_mapper
from utils import convert_price


class HomeAgent:

    """Docstring for Home. """
    
    def __init__(self):
        self._owner = None
        self._devices = dict()
        self._generators = dict()
        self._bill = 0

    def power(self, power_source, day, time):
        devs = list(self._devices.values())
        gens = list(self._generators.values())
        for d in devs:
            if d.is_plugged() and not d.is_charged():
            # It was like this before
            # if d.is_plugged():
                self.process_depending_on_goal(d, power_source, day, time)
    
    def process_depending_on_goal(self, dev, ps, d, t):
        if self._owner._ogoal == 'cost':
            curr_price = ps.get_current_price(d, t)
            owner = self.get_owner().get_name()
            price_limit = self._owner.get_preferences()[0]
            if curr_price >= price_limit:
                self.price_damage_control()
                print(f"[⚠️] Current price {float(curr_price)} is too high for household owned by {owner}!!!")
                return
        # Here we set conditions for other goals
        # elif self_owner._ogoal == 'other':
        
        # If everything is OK, charge device as intended
        dev.charge(self, ps)

    def price_damage_control(self):
        self.stop_charge_power_hungy_device()

    def stop_charge_power_hungy_device(self):
        devs = list(self._devices.values())
        charging_devs=  list(filter(lambda dev: dev.is_charging(), devs))
        if len(charging_devs):
            power_hungry_dev = reduce(lambda max_dev, dev: max_dev if max_dev.get_power_limit() > dev.get_power_limit() else dev, charging_devs)
            power_hungry_dev.stop_charge()

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
        nodes.append({
            'id': homeidx,
            'label': self._owner.get_name(),
            'title': f"{json.dumps(self.to_json(), indent = 2)}",
            'image': 'house-user-solid.png',
            'shape': 'image'
        })
        contidx += 1
        # Add devices and link them to home manager
        for d in self._owner.get_devices():
            charge = d.get_charge()
            nodes.append({
                'charge': charge,
                'id': contidx,
                'title': f" {json.dumps(d.to_json(), indent = 2)}",
                'color': color_mapper(charge)
            })
            # Change value to something meaningful
            if d.is_connected():
                e = {'id': contidx, 'from': contidx, 'to': homeidx}
                if d.is_charging():
                    e['color'] = 'rgb(166, 232, 44)'
                else:
                    e['color'] = 'rgb(100, 100, 100)'
                links.append(e)
            else:
                unlinks.append(contidx)
            # Increase counter (needed for Vis JS)
            contidx += 1

        return nodes, links, unlinks, contidx

    def to_string(self):
        devstr = ','.join(map(str, self._devices.keys()))
        genstr = ','.join(map(str, self._generators.keys()))
        return f"devices: {{{devstr}}}; genstr: {{{genstr}}}"
    
    def to_json(self):
        if self._owner._ogoal == 'cost':
            price_limit = self._owner.get_preferences()[0]
            obj = {
                '_entity_name': 'home',
                '_owner': self._owner.to_json(),
                '_price_limit': str(convert_price(price_limit)) + ' euro cents/kWh',
                '_bill': str(round(self.get_current_bill() / 100, 2)) + ' euros'
            }
        else:
            obj = {
                '_entity_name': 'home',
                '_owner': self._owner.to_json(),
                '_bill': str(round(self.get_current_bill() / 100, 2)) + ' euros'
            }
        return obj
