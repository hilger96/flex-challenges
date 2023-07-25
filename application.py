from flask import Flask, jsonify
import numpy as np
import sqlite3
import datetime

ç
app = Flask(__name__)

# Create API endpoints
@app.route('/v1/pnl/<strategy_id>', methods=['GET'])
def compute_pnl(strategy_id: str):
    
    conn = sqlite3.connect('trades.sqlite')
    cur = conn.cursor()
    
    # get quantity and price of all buys/sells where strategy='strategy_id'
    buys = cur.execute("SELECT quantity, price FROM 'epex_12_20_12_13' WHERE side = 'buy' AND strategy = '{}'".format(strategy_id)).fetchall()
    sells = cur.execute("SELECT quantity, price FROM 'epex_12_20_12_13' WHERE side = 'sell' AND strategy = '{}'".format( strategy_id)).fetchall()
    
    # calculate pnl
    pnl = - np.sum([np.prod(buys[i]) for i in range(len(buys))]) + np.sum([np.prod(sells[i]) for i in range(len(sells))])

    # get the present time as string according to definition
    tick = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # construct response dict
    response_data = {
        "strategy": strategy_id,
        "value": pnl,
        "unit": "euro",
        "capture_time": tick
    }

    # transform dictionary into json response according to definition.
    return jsonify(response_data), 200

