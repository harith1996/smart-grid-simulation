#!/usr/bin/python3

import random
import time
import numpy as np
from data import Device, User
from osbrain import run_agent
from osbrain import run_nameserver
from agents.device_agent import DeviceAgent;
from agents.user_agent import UserAgent;
from agents.home_agent import HomeAgent;
from agents.grid_agent import GridAgent;

if __name__ == '__main__':

    grid = None
    users, devices = [], []

    """
     _    ___   _   ___    ___   _ _____ _
    | |  / _ \ /_\ |   \  |   \ /_\_   _/_\
    | |_| (_) / _ \| |) | | |) / _ \| |/ _ \
    |____\___/_/ \_\___/  |___/_/ \_\_/_/ \_\

    """

    User.load_users("Users.json")
    Device.load_devices("Devices.json")

    ns = run_nameserver()

    grid = run_agent('Grid', base=GridAgent)

    symbols = "\|/-"
    symbidx = 0
    print(f"Loading data... {symbols[symbidx]}", end='\r')

    User.LUT = User.LUT[:2]

    for i, u in enumerate(User.LUT):

        # Create the user
        users.append(run_agent(base=UserAgent))
        
        # Create home manager
        home = run_agent(base=HomeAgent)
        home_ack_addr = home.bind('REP', alias='home_ack', handler='acknowledge_device')
        home_pub_addr = home.bind('PUB', alias='home_pub')

        # Create the user's list of devices
        devices = []
        for x in range(u['devices']):
            didx = random.randint(0, len(Device.LUT)-1)
            dev = run_agent(base=DeviceAgent)
            dev.connect(home_ack_addr, alias='home_ack')
            devices.append(dev)
            devices[x].set_attr(
                _did=didx,
                _name=Device.LUT[didx]['name'],
                _owner=u['name'],
                _load_profile=Device.LUT[didx]['load_profile'],
                _power_limit=Device.LUT[didx]['power_limit'],
                _capacity=Device.LUT[didx]['capacity'],
                _is_generator=Device.LUT[didx]['generator'],
                _curr_charge=Device.LUT[didx]['curr_charge'],
            )

        schedule = []
        for s in u['schedule']:
            days, times = s.split("/")
            day_start, day_end = days.split("-")
            hour_start, hour_end = times.split("-")

            day_start = int(day_start)
            day_end = int(day_end)
            hour_start = float(hour_start)
            hour_end = float(hour_end)

            schedule.append(((day_start, day_end),(hour_start, hour_end)))

        # Set the attributes for the user agent
        users[i].set_attr(
            _name=u['name'],
            _ogoal=u['ogoal'],
            _devices=devices,
            _schedule=schedule,
            _home_manager=home
        )

        symbidx = symbidx + 1 if symbidx < len(symbols) - 1 else 0
        print(f"Loading data... {symbols[symbidx]}", end='\r')

    """
     ___ _   _ _  _    ___ ___ __  __
    | _ \ | | | \| |  / __|_ _|  \/  |
    |   / |_| | .` |  \__ \| || |\/| |
    |_|_\\___/|_|\_|  |___/___|_|  |_|

    """
    step = 0.1
    for d in range(0, 7):
        print("- " * 30)
        print(f"\033[4mDAY Nº{d} STARTED!\033[0m")
        for t in np.arange(0.0, 24.0, step):
            t = round(t, 1)
            print(f"\n🕐 \033[1mTIME ⇒ {t}\033[0m\n")
            for u in users:
                u.run_devices(d, t)
                # We should manage home managers from the grid
                # but I will do this for testing
                u.trigger_home_manager()
            # time.sleep(.1)
            input()

    ns.shutdown()
