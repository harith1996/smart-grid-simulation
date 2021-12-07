import random
from typing import List

from agents.home import HomeAgent

class GridAgent:
    
    """Docstring for Grid. """
    
    #Average price of power in euro cents per watt second
    POWER_PRICE_AVG = 8.3e-6 

    #Maximum variance (+-) in price 
    POWER_PRICE_VAR = 2.7e-6

    #Pivot adjustment for weekends
    POWER_ADJ_WEEKEND = -1.1e-7

    
    #Pivot adjustment for peak hours
    POWER_ADJ_PEAK_HOURS = 2.2e-7

    def __init__(self):
        self._homes: List[HomeAgent] = []
        self._price_avg = GridAgent.POWER_PRICE_AVG
        self._price_var = GridAgent.POWER_PRICE_VAR
        self._current_load = 0

    def add_home(self, home):
        self._homes.append(home)
    
    def power_homes(self, d, t):
        curr_price = self.get_current_price(d, t)
        for h in self._homes:
            # We bill at the beginning
            # of each week for now
            if d == 0 and t == 0.0:
                owner = h.get_owner()
                print(f"[💰] Household owned by {owner.get_name()} received a bill of {h.get_power_draw(self) * curr_price}")
                h.reset_power_draw()
            h.power(self)
    
    def get_current_price(self, d, t):
        """Takes in day of week, and time of day to return current electricity price

        Args:
            d (integer): Day of week from 1 <= d <= 7
            t (float): Time of day from 0.0 <= t < 24.0 

        Returns:
            integer : Current price of electricity
        """
        if(d in [6,7]):
            self._price_avg += GridAgent.POWER_ADJ_WEEKEND
        if((t > 6 and t<8) or (t > 17 and t < 20)) :
            self._price_avg += GridAgent.POWER_ADJ_PEAK_HOURS
        return self._price_avg + (random.random() - 0.5) * self._price_var

    def update_billing(self, curr_price: float):
        """Updates electricity bill for all connected home managers

        Args:
            curr_price (float): current price of electricity
        """
        for hm in self._homes:
            curr_pw = hm.get_power_draw(self)
            hm.increment_bill(curr_pw * curr_price)

    def show_bills(self):
        for h in self._homes:
                owner = h.get_owner()
                print(f"[💰] Household owned by {owner.get_name()} received a bill of {round(h.get_current_bill() / 100, 2)} euros")
    
    def increment_load(self, load):
        self._current_load+=load
    
    def to_graph(self, contidx):
        nodes, links = [], []
        # Add grid
        grididx = contidx
        nodes.append({'id': grididx, 'image': 'charging-station-solid.png', 'shape': 'image', 'value': 30})
        contidx += 1
        # Add home managers and their devices.
        # Also link home managers to grid.
        for h in self._homes:
            links.append({'from': contidx, 'to': grididx})
            # Change value to something meaningful
            hnodes, hlinks, contidx = h.to_graph(contidx)
            nodes.extend(hnodes)
            links.extend(hlinks)

        return nodes, links, contidx

    def to_string(self):
        pass
