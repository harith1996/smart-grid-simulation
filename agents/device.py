from numpy import empty
from luts import Device

class DeviceAgent:

    """Docstring for Device. """
    
    UID = 0
    
    def __init__(self, did, owner, init_charge):
        # Initialize attributes
        self._uid = DeviceAgent.UID # Unique ID
        self._did = did # Device ID
        self._owner = owner
        self._curr_charge = round(init_charge, 4)
        self._t2c = -1
        self._plugged = False
        self._conn_to_dev_channel = False
        self._conn_to_gen_channel = False
        self._is_charging = False
        self._power_source = 0
        DeviceAgent.UID += 1

    def plug(self, home, t2c):

        self._t2c = round(t2c, 4)
        self._plugged = True

        # If device can provide power, we should initalize
        # some sort of connection here and pass it on to the
        # manager so that it can send the address to other devices

        # Send info to HomeAgent
        self._conn_to_dev_channel, self._conn_to_gen_channel = home.acknowledge_device(self)

        # If everything is OK, subscribe to home manager
        if self._conn_to_dev_channel or self._conn_to_gen_channel:
            print(f"[🔌] {self._owner.get_name()} plugs {self.to_string()} and ACK is accepted \033[92m✔️\033[0m")
        else:
            print(f"[🔌] {self._owner.get_name()} plugs {self.to_string()} and ACK is NOT accepted \033[91m✖️\033[0m")
    
    def unplug(self, home):
        self._plugged = False
        
        if self._conn_to_dev_channel:
            home.disconnect_device(self)
            self._conn_to_dev_channel = False
        
        if self._conn_to_gen_channel:
            # Generator disconnects completely from home manager.
            # A generator has to be connected at all times
            # regardless of whether it's charged or not.
            # Obviously when it's in use it will
            # unplug and disconnect.
            home.disconnect_generator(self)
            self._conn_to_gen_channel = False
            
    def charge(self, home, power_source, t = 0.1 ):

        self._t2c = max(round(self._t2c - t, 4), 0.0)
        
        charge_increment = self.get_charge_profile() * t
        new_charge = self._curr_charge + charge_increment
        power_draw = self.get_power_limit()
        
        if new_charge < 1.0:
            self._curr_charge = round(new_charge, 4)
            self._is_charging = True
            self._power_source = power_source
            self._power_source.connect_power(self.get_power_limit())
            print(f"[⚡️] {self._owner.get_name()}'s {self.to_string()} is charging")
        else:
            self._curr_charge = 1.0
            self._is_charging = False
            self.disconnect_from_power_source()
            print(f"[🏁] {self._owner.get_name()}'s {self.to_string()} finished charging")
            # We close connection with the home manager
            # if device is completely charged
            # Generators will still be connected to the
            # manager still.
            self._conn_to_dev_channel = home.disconnect_device(self)
        
        return power_draw

    # By default we decrease one unit
    def discharge(self, t = 0.1):
        
        self._is_charging = False
        if self._curr_charge == 0.0:
            return

        new_charge = self._curr_charge - self.get_charge_profile() * t

        if new_charge > 0.0:
            self._curr_charge = round(new_charge, 4)
            print(f"[🔋] {self._owner.get_name()} uses {self.to_string()}")
        else:
            self._curr_charge = 0.0
            print(f"[❌] {self._owner.get_name()} depleated {self.to_string()}")

    def is_plugged(self):
        return self._plugged

    def is_connected(self):
        # return self._conn_to_dev_channel, self._conn_to_gen_channel
        return self._conn_to_dev_channel or self._conn_to_gen_channel

    def is_charged(self):
        return self._curr_charge == 1.0

    def is_depleated(self):
        return self._curr_charge == 0.0

    def is_generator(self):
        return Device.LUT[self._did]['generator']
    
    def get_charge(self):
        return self._curr_charge
    
    def get_name(self):
        return Device.LUT[self._did]['name']

    def get_type(self):
        return Device.LUT[self._did]['type']

    def get_power_limit(self):
        return round(float(Device.LUT[self._did]['power_limit']), 1)

    def get_charge_profile(self):
        return round(Device.LUT[self._did]['charge_profile'], 4)

    def to_string(self):
        return f"{{uid: {self._uid}; did: {self._did}; is_gen: {self.is_generator()}; " \
                f"charge_prof: {self.get_charge_profile()} % per second; curr_charge: {self._curr_charge}; %" \
                f"t2c: {self._t2c}}}"

    def toJSON(self):
        return {
            '_uid': self._uid,
            '_name': self.get_name(),
            '_did': self._did,
            '_owner': self._owner.get_name(),
            '_type': self.get_type()
        }
