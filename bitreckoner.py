# vim: set fileencoding=utf8 :

import requests
import json
import argparse
import hashlib
import time
import tempfile
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("--address", action="store", required=True)
parser.add_argument("--no-cache", action="store_true", default=False)
parser.add_argument("--start", action="store", default=None)
parser.add_argument("--end", action="store", default=None)
args = parser.parse_args()

start = time.mktime(time.strptime(args.start, "%Y-%m-%d")) if args.start \
    is not None else 0
end = time.mktime(time.strptime(args.start, "%Y-%m-%d")) if args.end is \
    not None else 2**32

transaction_url_format = "https://blockchain.info/address/%s?format=json"
price_url = "https://api.bitcoinaverage.com/history/EUR/per_day_all_time_history.csv"

def fetch(url, args):
    cache_path = os.path.join(tempfile.gettempdir(),
        "%s.%s" % (hashlib.md5(url).hexdigest(), sys.argv[0]))
    
    if not args.no_cache and os.path.exists(cache_path):
        return open(cache_path).read()

    response = requests.get(url)

    if response.status_code == 200:
        if not args.no_cache:
            open(cache_path, "w").write(response.content)

        return response.content
    else:
        raise RuntimeError("Got HTTP %d for %s, expected 200",
            response.status_code, url)

# Load the price history.
price_history_csv = fetch(price_url, args)

# Build a dictionary of date => average price
prices = {}
for line in price_history_csv.split("\n")[1:]:
    if len(line) == 0:
        continue
    datetm, high, low, average, volume = line.split(",")
    date, tm = datetm.split(" ")
    prices[date] = float(average)

# Load transactions.
addrhistory_json = fetch(transaction_url_format % args.address, args)
addrhistory = json.loads(addrhistory_json)

# Dump a table of the transactions, their values at transaction time and
# a running total.
eur_value_total = 0
for transaction in addrhistory['txs'][::-1]:
    # Skip transactions outside the specified start/end dates.
    if not (start < transaction['time'] < end):
        continue

    # Sum all the values of all the outputs that are assigned to this address.
    satoshi_value = sum([output['value'] for output in transaction['out']
        if output['addr'] == args.address])

    # Convert from an integer number of satoshis to a float BTC.
    btc_value = satoshi_value * 0.00000001

    # Look up the price on the day of the transaction and calculate the euro
    # equivalent, and add it to the running total.
    date = time.strftime("%Y-%m-%d", time.gmtime(transaction['time']))
    eur_value = prices[date] * btc_value
    eur_value_total += eur_value

    print "%s %.8f  €% 8.2f  €% 8.2f" % (
        time.ctime(transaction['time']), btc_value, eur_value,
        eur_value_total)



