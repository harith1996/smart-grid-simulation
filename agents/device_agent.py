import json
from osbrain import Agent

class DeviceAgent(Agent):

    """Docstring for Device. """

    def on_init(self):
        # Initialize attributes
        self._did = -1
        self._name = None
        self._owner = None
        # self._power_limit = 1
        # self._capacity = 100
        self._load_profile = 0.0001
        self._curr_charge = 0
        self._t2c = -1
        self._plugged = False
        self._is_generator = False

    def plug(self, t, t2c):

        self._t2c = t2c
        self._plugged = True

        # If device can provide power, we should initalize
        # some sort of connection here and pass it on to the
        # manager so that it can send the address to other devices

        # Send info to HomeAgent
        info = {
            'did': self._did,
            'load_profile': self._load_profile,
            'curr_charge': self._curr_charge,
            'generator': self._is_generator,
            't2c': self._t2c
        }
        ok, sub_addr = self.send_recv('home_ack', info)
        # If everything is OK, subscribe to home manager
        if ok:
            print(f"[🔌] {self._owner} plugs {self.to_string()} and ACK is accepted ✅")
            topic = f"charge-{self._did}"
            self.connect(sub_addr, alias='home_sub', handler={topic: self.charge})
        else:
            print(f"[🔌] {self._owner} plugs {self.to_string()} and ACK is NOT accepted ❌")

    def charge(self, msg):

        # If device is charged and it's a generator, we
        # stay connected but we don't charge
        if self._curr_charge == 1.0 and self._is_generator:
            return

        new_charge = self._curr_charge + self._load_profile

        if new_charge < 1.0:
            self._curr_charge = round(new_charge, 4)
            print(f"[⚡️] {self._owner}'s {self.to_string()} is charging")
        else:
            self._curr_charge = 1.0
            print(f"[🏁] {self._owner}'s {self.to_string()} finished charging")
            # We close connection with the home manager
            # if device is completely charged
            if not self._is_generator:
                # topic = f"charge-{self._did}"
                # self.unsubscribe('home_sub', topic)
                self.close('home_sub')

    # By default we decrease one unit
    def discharge(self):

        # Generator disconnects from home manager.
        # A generator has to be connected at all times
        # regardless of whether it's charged or not
        if self._is_generator:
            # topic = f"charge-{self._did}"
            # self.unsubscribe('home_sub', topic)
            self.close('home_sub')

        self._plugged = False

        if self._curr_charge == 0:
            return

        new_charge = self._curr_charge - self._load_profile

        if new_charge > 0.0:
            self._curr_charge = round(new_charge, 4)
            print(f"[🔋] {self._owner} uses {self.to_string()}")
        else:
            self._curr_charge = 0.0
            print(f"[❌] {self._owner} depleated {self.to_string()}")

    def is_plugged(self):
        return self._plugged

    def is_charged(self):
        return self._curr_charge == 1.0

    def is_depleated(self):
        return self._curr_charge == 0.0

    def to_string(self):
        return f"{{Id: {self._did}; Name: {self._name}; " \
                f"Load profile: {self._load_profile}; Current charge: {self._curr_charge}; " \
                f"Time to charge: {self._t2c}}}"
