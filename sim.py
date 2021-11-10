#!/usr/bin/python3

import random
from data import Device, User
from osbrain import run_agent
from osbrain import run_nameserver
from agents import GridAgent, DeviceAgent, UserAgent

if __name__ == '__main__':

    grid = None
    users, devices = [], []
    
    User.load_users("Users.json")
    Device.load_devices("Devices.json")

    ns = run_nameserver()

    grid = run_agent('Grid', base=GridAgent)
    
    for i, u in enumerate(User.LUT):

        # Create the user
        users.append(run_agent(base=UserAgent))

        # Create the user's list of devices
        devices = []
        for x in range(u['ndevices']):
            didx = random.randint(0, len(Device.LUT)-1)
            devices.append(run_agent(base=DeviceAgent))
            devices[x].set_attr(
                _did=didx,_name=Device.LUT[didx]['name'],
                _load_profile=Device.LUT[didx]['load_profile'],
                _power_limit=Device.LUT[didx]['power_limit'],
                _capacity=Device.LUT[didx]['capacity']
            )
            
        # Set the attributes for the user agent
        users[i].set_attr(_name=u['name'],_ogoal=u['ogoal'],_devices=devices)
        print(users[i].to_string())

    ns.shutdown()
