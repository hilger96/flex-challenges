from flask import Flask, jsonify
import numpy as np
import sqlite3
import datetime




app = Flask(__name__)

# Create the API endpoint.
@app.route('/v1/pnl/<strategy_id>', methods=['GET'])
def compute_pnl(strategy_id: str):
    
    conn = sqlite3.connect('trades.sqlite')
    cur = conn.cursor()
    buys = cur.execute("SELECT quantity, price FROM 'epex_12_20_12_13' WHERE side = 'buy' AND strategy = '{}'".format(strategy_id)).fetchall()
    sells = cur.execute("SELECT quantity, price FROM 'epex_12_20_12_13' WHERE side = 'sell' AND strategy = '{}'".format( strategy_id)).fetchall()
    
    pnl = - np.sum([np.prod(buys[i]) for i in range(len(buys))]) + np.sum([np.prod(sells[i]) for i in range(len(sells))])

    tick = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    response_data = {
        "strategy": strategy_id,
        "value": pnl,
        "unit": "euro",
        "capture_time": tick
    }

    return jsonify(response_data), 200



# app = Flask(__name__)

# def compute_pnl(strategy_id: str):
    
#     conn = sqlite3.connect('trades.sqlite')
#     cur = conn.cursor()
#     buys = cur.execute("SELECT quantity, price FROM 'epex_12_20_12_13' WHERE side = 'buy' AND strategy = '{}'".format(strategy_id)).fetchall()
#     sells = cur.execute("SELECT quantity, price FROM 'epex_12_20_12_13' WHERE side = 'sell' AND strategy = '{}'".format( strategy_id)).fetchall()
    
#     pnl = - np.sum([np.prod(buys[i]) for i in range(len(buys))]) + np.sum([np.prod(sells[i]) for i in range(len(sells))])

#     return(pnl)


# # Create the API endpoint.
# @app.route('/v1/pnl/<strategy_id>', methods=['GET'])
# def get_response_data(strategy_id):

#     result = compute_pnl(strategy_id=strategy_id)

#     tick = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

#     response_data = {
#         "strategy": strategy_id,
#         "value": result,
#         "unit": "euro",
#         "capture_time": tick
#     }

#     return jsonify(response_data), 200