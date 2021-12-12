import random
import statistics
from typing import List

from agents.home import HomeAgent
from utils import convert_price

class GridAgent:
    
    """Docstring for Grid. """
    
    #Average price of power in euro cents per watt second
    POWER_PRICE_AVG = 8.3e-6 

    #Maximum variance (+-) in price 
    POWER_PRICE_VAR = 2.7e-6

    #Pivot adjustment for weekends
    POWER_ADJ_WEEKEND = -1.1e-7

    #Pivot adjustment for crossing load limit
    POWER_ADJ_LOAD_LIMIT = 8.3e-6
    
    #Pivot adjustment for peak hours
    POWER_ADJ_PEAK_HOURS = 2.2e-7

    #Grid Capacity (kiloWatts)
    LOAD_LIMIT = 500

    def __init__(self, seed):
        self._homes: List[HomeAgent] = []
        self._price_avg = GridAgent.POWER_PRICE_AVG
        self._price_var = GridAgent.POWER_PRICE_VAR
        self._current_load = 0
        self._peak_load = 0
        self._load_limit = GridAgent.LOAD_LIMIT * 1000
        random.seed(seed)
        self._rnd_state = random.getstate()
        self._bill_avg = 0
        self._bill_var = 0
        self._top_bill = 0

    def add_home(self, home):
        self._homes.append(home)
    
    def power_homes(self, d, t):
        random.setstate(self._rnd_state)
        curr_price = self.get_current_price(d, t)
        for h in self._homes:
            # We bill at the beginning
            # of each week for now
            if d == 0 and t == 0.0:
                owner = h.get_owner()
                print(f"[💰] Household owned by {owner.get_name()} received a bill of {h.get_power_draw(self) * curr_price}")
                h.reset_power_draw()
            h.power(self, d , t)
        self._rnd_state = random.getstate()
    
    def get_current_price(self, d, t):
        """Takes in day of week, and time of day to return current electricity price

        Args:
            d (integer): Day of week from 1 <= d <= 7
            t (float): Time of day from 0.0 <= t < 24.0 

        Returns:
            integer : Current price of electricity
        """
        random.setstate(self._rnd_state)
        self._price_avg = GridAgent.POWER_PRICE_AVG
        # Weekend Adjustment
        if(d in [6, 7]):
            self._price_avg += GridAgent.POWER_ADJ_WEEKEND

        # Time of day adjustment
        if((t > 6 and t < 8) or (t > 17 and t < 20)):
            self._price_avg += GridAgent.POWER_ADJ_PEAK_HOURS

        # Load  limit adjustment
        if(self._current_load > self._load_limit):
            self._price_avg += GridAgent.POWER_ADJ_LOAD_LIMIT

        self._rnd_state = random.getstate()
        return self._price_avg + (random.random() - 0.5) * 2 * self._price_var

    def update_billing(self, curr_price: float):
        """Updates electricity bill for all connected home managers

        Args:
            curr_price (float): current price of electricity
        """
        self.increment_bills(curr_price)
        self.compute_bill_statistics()

    def compute_bill_statistics(self):
        bills = list(map(lambda home: home.get_current_bill(), self._homes))
        self._bill_avg = statistics.mean(bills)
        self._bill_var = statistics.variance(bills)
        self._top_bill = max(bills)

    def increment_bills(self, curr_price): 
        for hm in self._homes:
            curr_pw = hm.get_power_draw(self)
            hm.increment_bill(curr_pw * curr_price)

    def show_bills(self):
        for h in self._homes:
                owner = h.get_owner()
                print(f"[💰] Household owned by {owner.get_name()} received a bill of {round(h.get_current_bill() / 100, 2)} euros")
    
    def get_bills(self):
        out = []
        for h in self._homes:
            owner_name = h.get_owner().get_name()
            bill = round(h.get_current_bill() / 100, 2)
            out.append( {
                "home_owner": owner_name,
                "bill_amount": bill
            })
        return out

    def increment_load(self, load):
        self._current_load += load
    
    def to_graph(self, contidx):
        nodes, links, unlinks = [], [], []
        # Add grid
        grididx = contidx
        nodes.append({'id': grididx, 'image': 'charging-station-solid.png', 'shape': 'image', 'value': 30})
        contidx += 1
        # Add home managers and their devices.
        # Also link home managers to grid.
        for h in self._homes:
            links.append({'id': contidx, 'from': contidx, 'to': grididx})
            # Change value to something meaningful
            hnodes, hlinks, hunlinks, contidx = h.to_graph(contidx)
            nodes.extend(hnodes)
            links.extend(hlinks)
            unlinks.extend(hunlinks)

        return nodes, links, unlinks, contidx

    def connect_power(self, power_limit):
        """Called by a device when charging.

        Args:
            power_limit (int): Max power drawn by the device

        Returns:
            Boolean: True if device is allowed to connect
        """
        self._current_load += power_limit
        if(self._peak_load < self._current_load):
            self._peak_load = self._current_load
        return True

    def disconnect_power(self, power_limit):
        """Called by a device when disconnecting from grid.

        Args:
            power_limit (int): Max power drawn by the device

        Returns:
            Boolean: True if device can safely disconnect
        """
        self._current_load -= power_limit
        return True

    def get_homes(self):
        return self._homes

    def to_json(self):
        homes = list(map(lambda home: home.to_json(), self._homes))
        return {
            '_entity_name': 'grid',
            '_price_avg': convert_price(GridAgent.POWER_PRICE_AVG),
            '_price_var': convert_price(GridAgent.POWER_PRICE_VAR),
            '_load_limit': self._load_limit / 1000,
            '_homes': homes,
            '_homes_connected': len(homes)
        }

    def get_status_JSON(self, current_price):
        return {
            '_peak_load': self._peak_load / 1000,
            '_current_load': self._current_load / 1000,
            '_current_price': round(convert_price(current_price), 2)
        }

    def get_bill_statistics_JSON(self):
        return {
            '_bill_avg': round(self._bill_avg/100 , 2),
            '_bill_var': round(self._bill_var/100, 2),
            '_top_bill': round(self._top_bill/100, 2)
        }
