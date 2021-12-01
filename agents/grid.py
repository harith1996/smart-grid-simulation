import random

class GridAgent:

    """Docstring for Grid. """
    
    #Average price of power in euro cents/kWh
    POWER_PRICE_AVG = 30

    #Maximum variance (+-) in price 
    POWER_PRICE_VAR = 10

    def __init__(self):
        self._homes = []
        self._price_avg = GridAgent.POWER_PRICE_AVG
        self._price_var = GridAgent.POWER_PRICE_VAR

    def add_home(self, home):
        self._homes.append(home)
    
    def power_homes(self, d, t):
        curr_price = self.get_current_price(d, t)
        for h in self._homes:
            # We bill at the beginning
            # of each week for now
            if d == 0 and t == 0.0:
                owner = h.get_owner()
                print(f"[💰] Household owned by {owner.get_name()} received a bill of {h.get_power_draw() * curr_price}")
                h.reset_power_draw()
            h.power()
    
    def get_current_price(self, d, t):
        """Takes in day of week, and time of day to return current electricity price

        Args:
            d (integer): Day of week from 1 <= d <= 7
            t (float): Time of day from 0.0 <= t < 24.0 

        Returns:
            integer : Current price of electricity
        """
        if(d in [6,7]):
            self._price_avg -=4
        if((t > 6 and t<8) or (t > 17 and t < 20)) :
            self._price_avg +=8
        return self._price_avg + (random.random() - 0.5) * self._price_var

    def to_string(self):
        pass