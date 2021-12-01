class GridAgent:

    """Docstring for Grid. """

    def __init__(self):
        self._homes = []

    def add_home(self, home):
        self._homes.append(home)
    
    def power_homes(self):
        for h in self._homes:
            h.power()

    def to_string(self):
        pass