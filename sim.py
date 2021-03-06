#!/usr/bin/python3

# Flask
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask.helpers import send_file

# Other Python stuff
import json
import numpy as np
from luts import User
from agents.grid import GridAgent
from data import load_data_from_object, load_data_from_file

STEP = 0.1

# Each connected user will store it's data here
simuserdata = dict()
app = Flask(__name__,
        static_url_path='', 
        static_folder='web/')
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_file('web/index.html')

@socketio.on('init')
def init_sim(info):
    userid = info.get('userid') 
    data = info.get('data')
    ogoal = info.get('ogoal')
    
    # Does the user send custom data ?
    if data:
        grid, users = load_data_from_object(json.loads(data))
    else:
        grid, users = load_data_from_file("data.json")

    for u in users:
        u.use_devices(0, 0.0)

    # Does the user want to override the optimization goal ?
    if ogoal:
        goal = User.OGOAL[ogoal]
        for h in grid.get_homes():
            u = h.get_owner()
            u.set_ogoal(goal)

    grid.power_homes(0, 0.0)
    current_price = grid.get_current_price(0, 0.0)
    grid.update_billing(current_price)
    nodes, edges, _, _ = grid.to_graph(0)

    # Grid, Users, Time of the day, Day of the Week, Day of the Year
    simuserdata[userid] = [grid, users, 0.1, 0, 0]
    emit('get-grid-status-res', grid_status(info, current_price))
    emit('init-res', {
        'nodes': nodes,
        'edges': edges,
        'ct': 0.1,
        'cdw': 0,
        'cdy': 0
    })

@socketio.on('update')
def update_sim(info):
    userid = info.get('userid') 
    # Grid, Users, Time of the day, Day of the Week, Day of the Year
    ct = simuserdata[userid][2]
    cdw = simuserdata[userid][3]
    cdy = simuserdata[userid][4]
    for u in simuserdata[userid][1]:
        u.use_devices(cdw, ct)
    simuserdata[userid][0].power_homes(cdw, ct)
    current_price = simuserdata[userid][0].get_current_price(cdw, ct)
    simuserdata[userid][0].update_billing(current_price)
    nodes, edges, unlinks, _ = simuserdata[userid][0].to_graph(0)
    
    ct += STEP 

    if ct >= 24.0:
        ct = 0.0
        cdw += 1
        cdy += 1
    if cdw >= 7:
        # In this case we stop the
        # the simulation when we
        # reach the end of the week.
        nodes, edges = [], []
        cdw = 0
    if cdy >= 365:
        cdy = 0

    simuserdata[userid][2] = ct 
    simuserdata[userid][3] = cdw
    simuserdata[userid][4] = cdy

    emit('get-bill-statistics-res', get_bill_statistics(info))
    emit('get-grid-status-res', grid_status(info, current_price))
    emit('update-res', {
        'nodes': nodes,
        'edges': edges,
        'unlinks': unlinks,
        'ct': round(ct,1),
        'cdw': cdw,
        'cdy': cdy
    })

@socketio.on('skip')
def skip_sim(info):
    
    userid = info.get('userid') 
    grid : GridAgent = simuserdata[userid][0]
    users = simuserdata[userid][1]
    ct = simuserdata[userid][2]
    cdw = simuserdata[userid][3]
    cdy = simuserdata[userid][4]
    dw = cdw
    t = ct
    for dw in range(cdw, 7):
        for t in np.arange(ct, 24.0, STEP):
            t = round(t, 1)
            for u in users:
                u.use_devices(dw, t)
            grid.power_homes(dw, t)
            grid.update_billing(grid.get_current_price(dw, t))
    
    nodes, edges, unlinks, _ = grid.to_graph(0)

    simuserdata.pop(userid)
    emit('get-bill-statistics-res', grid.get_bill_statistics_JSON())
    emit('get-grid-status-res', grid.get_status_JSON(grid.get_current_price(dw,t)))
    emit('skip-res', {'nodes': nodes, 'edges': edges, 'unlinks': unlinks})

@socketio.on('get-grid-info')
def get_grid_info(info):
    emit('get-grid-info-res', grid_info(info))

def grid_status(info, current_price):
    """Returns current status of the grid: Current load, peak load, current price

    Returns:
        [type]: [description]
    """
    userid = info.get('userid') 
    grid : GridAgent = simuserdata[userid][0]
    
    return grid.get_status_JSON(current_price)

def grid_info(info):
    userid = info.get('userid') 
    grid : GridAgent = simuserdata[userid][0]
    print(userid)
    """Returns static info about the grid: Homes, Users, Devices, Grid Capacity, Prive average, Price Variance

    Returns:
        [type]: [description]
    """
    return grid.to_json()

    
def get_bill_statistics(info):
    userid = info.get('userid') 
    grid : GridAgent = simuserdata[userid][0]
    print(userid)
    """Returns statistics of home bills: Average home bill, variance and highest bill

    Returns:
        [type]: [description]
    """
    return grid.get_bill_statistics_JSON()

if __name__ == '__main__':

    """
     ___ _   _ _  _    ___ ___ __  __
    | _ \ | | | \| |  / __|_ _|  \/  |
    |   / |_| | .` |  \__ \| || |\/| |
    |_|_\\___/|_|\_|  |___/___|_|  |_|

    """

    socketio.run(app)
