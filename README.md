# BitReckoner

A small tool for matching a list of bitcoin transactions with the approximate euro price on the day of the transaction. Intended for when you have a bitcoin address that mostly receives over a long period, and you'd like to know what the approximate euro transaction values were.

## Features

* Single python file.
* Light dependencies, just python-requests.
* Takes a bitcoin address as input from the user.
* Can be limited by start and end dates.
* Uses the blockchain.info API for transaction data.
* Uses the bitcoinaverage.com API for historical price data.
* Caches transaction and price data in /tmp.

## Usage

```shell
$ python bitreckoner.py --help
usage: bitreckoner.py [-h] --address ADDRESS [--no-cache] [--start START]
                      [--end END]

optional arguments:
  -h, --help         show this help message and exit
  --address ADDRESS
  --no-cache
  --start START
  --end END
$ python bitreckoner.py --address 1GwfazTSHfFnUmWiRDj6Fb46h7BcK1fDCw
Fri Jan  8 23:00:27 2016 0.05100000  €   21.35  €   21.35
Fri Jan  8 23:37:35 2016 0.00000000  €    0.00  €   21.35
Fri Jan  8 23:58:54 2016 0.05100000  €   21.35  €   42.70
Sat Jan  9 03:15:17 2016 0.00000000  €    0.00  €   42.70
$ python bitreckoner.py --address 1GwfazTSHfFnUmWiRDj6Fb46h7BcK1fDCw --start 2016-01-09
Sat Jan  9 03:15:17 2016 0.00000000  €    0.00  €    0.00
```

## Issues

* Makes no attempt to filter transactions where the provided address is used as an input.
* Makes no attempt to adjust the running total as inputs are spent.
* Euro is hardcoded. USD support is easy but not implemented yet.
* The cache timeout is infinite, requiring the user to use --no-cache or to delete the cache files from /tmp.

## Contributions

Pull requests and forks welcome, but I may not have time to fix bugs and deal with github issues, so expect limited support.

## License

See LICENSE
