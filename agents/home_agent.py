import json
from osbrain import Agent

class HomeAgent(Agent):

    """Docstring for Home. """

    def on_init(self):
        self._sub_addr = self.bind('PUB', alias='home_sub')

    def check_for_generator(self):
        pass

    def power_devices(self):
        # Send message to last connected device
        # (testing things out)
        topic = f"charge-{self._some_did}"
        self.send('home_sub', 'yay', topic=topic)

    def acknowledge_device(self, info):
        # We should do something with the info
        self._some_did = info['did']
        return (True, self._sub_addr)
