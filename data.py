import random
from luts import User, Device
from agents.device import DeviceAgent
from agents.user import UserAgent
from agents.home import HomeAgent
from agents.grid import GridAgent

def load_data(userjson, devjson):
    """Dumps data from JSONs to look up tables and returns grid.


    Args:
        userjson (str): Filename of the user's json.
        devjson (str): Filename of the devices' json.

    Returns:
        [tuple]: Returns the grid and users.
    """

    grid = None
    users = []

    User.load_users(userjson)
    Device.load_devices(devjson)

    grid = GridAgent()

    symbols = "\|/-"
    symbidx = 0
    print(f"Loading data... {symbols[symbidx]}", end='\r')
    
    # change !!!!!
    User.LUT = User.LUT[:3]
    
    for i, u in enumerate(User.LUT):

        # Create the home and user
        home = HomeAgent()
        user = UserAgent(u['name'], home, u['ogoal'])
        
        # Create the user's list of devices
        devices = []
        for x in range(u['devices']):
            didx = random.randint(0, len(Device.LUT)-1)
            dev = DeviceAgent(didx, user, Device.LUT[didx]['curr_charge'])

            s = u['schedule'][x]
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