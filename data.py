import random
import json
from luts import User, Device
from agents.device import DeviceAgent
from agents.user import UserAgent
from agents.home import HomeAgent
from agents.grid import GridAgent

def load_data_from_object(data):
    """Dumps data from JSONs to look up tables and returns grid.


    Args:
        userjson (str): Filename of the user's json.
        devjson (str): Filename of the devices' json.

    Returns:
        [tuple]: Returns the grid and users.
    """

    Device.LUT = data['devices']
    User.LUT = data['users']

    grid = GridAgent()
    users = []

    symbols = "\|/-"
    symbidx = 0
    print(f"Loading data... {symbols[symbidx]}", end='\r')
    
    for i, u in enumerate(User.LUT):

        # Create the home and user
        home = HomeAgent()
        user = UserAgent(u['name'], home, u['ogoal'])
        
        home.set_owner(user)
        
        # Get the user's list of devices
        for i, v in enumerate(u['devices']):

            dev = DeviceAgent(v, user, Device.LUT[v]['curr_charge'])

            s = u['schedules'][i]
            days, times = s.split("/")
            day_start, day_end = days.split("-")
            hour_start, hour_end = times.split("-")

            day_start = int(day_start)
            day_end = int(day_end)
            hour_start = float(hour_start)
            hour_end = float(hour_end)
            
            user.add_device(dev, ((day_start, day_end),(hour_start, hour_end)))

        users.append(user)
        grid.add_home(home)

        symbidx = symbidx + 1 if symbidx < len(symbols) - 1 else 0
        print(f"Loading data... {symbols[symbidx]}", end='\r')
    
    return grid, users

def load_data_from_file(file):
    """Dumps data from JSONs to look up tables and returns grid.


    Args:
        userjson (str): Filename of the user's json.
        devjson (str): Filename of the devices' json.

    Returns:
        [tuple]: Returns the grid and users.
    """

    grid = None
    users = []

    file = open(file, "r") 
    data = json.load(file)
    file.close()
    
    return load_data_from_object(data)