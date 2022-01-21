import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def orderBook(symbol, limit = 1000):
    url = 'https://dapi.binance.com/dapi/v1/depth'
    params = {'symbol' : symbol}
    r = requests.get(url, params=params)
    results = r.json()

    value_bidsDF = pd.DataFrame(data=results["bids"], columns=["price", "quantity"], dtype=float)
    value_asksDF = pd.DataFrame(data=results["asks"], columns=["price", "quantity"], dtype=float)
    frames = {
        "bids": value_bidsDF,
        "asks": value_asksDF,
        }

    asksDF = frames["asks"].assign(side = "ask")
    bidsDF = frames["bids"].assign(side = "bids")
    frames_list = [asksDF, bidsDF]
    data = pd.concat(frames_list, axis = 'index', ignore_index= True, sort = True)
    price_summary = data.groupby("side").price.describe()
    return data, price_summary

def graph(data):
    fig, ax = plt.subplots()

    #ax.set_title(f"Last update: {t} (ID: {last_update_id})")

    sns.scatterplot(x="price", y="quantity", hue="side", data=data, ax=ax)

    ax.set_xlabel("Price")
    ax.set_ylabel("Quantity")

    plt.show()







resDF, resPerc = orderBook('BTCUSD_PERP', limit = 1000)
print(resPerc)
graph(resDF)
