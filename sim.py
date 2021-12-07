#!/usr/bin/python3

from flask import Flask, jsonify
from flask.helpers import send_file
import numpy as np
import time
from data import load_data

STEP = 0.1

"""
 _    ___   _   ___    ___   _ _____ _
| |  / _ \ /_\ |   \  |   \ /_\_   _/_\
| |_| (_) / _ \| |) | | |) / _ \| |/ _ \
|____\___/_/ \_\___/  |___/_/ \_\_/_/ \_\

"""
grid, users = load_data("Users.json", "Devices.json")
app = Flask(__name__,
        static_url_path='', 
        static_folder='web/')

@app.route('/')
def index():
    return send_file('web/index.html')

@app.route('/data')
def data():
    # We only have one grid for now, but we would
    # continue to use contidx if we used more grids
    nodes, links, contidx = grid.to_graph(0)
    return jsonify({
        'nodes': nodes,
        'edges': links
    })

if __name__ == '__main__':

    """
     ___ _   _ _  _    ___ ___ __  __
    | _ \ | | | \| |  / __|_ _|  \/  |
    |   / |_| | .` |  \__ \| || |\/| |
    |_|_\\___/|_|\_|  |___/___|_|  |_|

    """
    # Should we support leap years ? xD
    # for dy in range(0, 365):
    """
    for dw in range(0, 7):
        print("- " * 30)
        print(f"\n\033[4mDAY Nº{dw} STARTED!\033[0m")
        for t in np.arange(0.0, 24.0, STEP):
            t = round(t, 1)
            print(f"\n🕐 \033[1mTIME ⇒ {t}\033[0m\n")
            for u in users:
                u.use_devices(dw, t)
            grid.power_homes(dw, t)
            grid.update_billing(grid.get_current_price(dw, t))
            # time.sleep(0.2)
    """
    for u in users:
        u.use_devices(0, 0.0)
    grid.power_homes(0, 0.0)
    grid.update_billing(grid.get_current_price(0, 0.0))
    # time.sleep(0.2)
    grid.show_bills()
    app.run()