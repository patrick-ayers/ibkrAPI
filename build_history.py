''' Demonstrates how an application can request the current time '''

import ib_insync
import pandas as pd
from contracts import equities, futures, currencies
from os.path import exists


def drop_duplicates_from_csv(csv_location):
    df = pd.read_csv(csv_location)
    df = df.drop_duplicates(subset=['date'], keep='last')
    df.to_csv(csv_location)


def create_new(contract, file_name):
    bar_length_to_duration = {'1 hour': '1 M', '5 mins': '10 D', '1 min': '5 D'}

    for bar_length in ['1 min', '5 mins', '1 hour']:
        for contracts in [currencies, futures, equities]:
            for contract in contracts:
                dt = ''
                barsList = []
                what_to_show = 'MIDPOINT' if contract.exchange == 'IDEALPRO' else 'TRADES'
                output_symbol = contract.pair() if contract.exchange == 'IDEALPRO' else contract.symbol
                while True:
                    bars = ib.reqHistoricalData(
                        contract,
                        endDateTime=dt,
                        durationStr=bar_length_to_duration[bar_length],
                        barSizeSetting=bar_length,
                        whatToShow=what_to_show,
                        useRTH=False,
                        formatDate=2)
                    if not bars:
                        break
                    barsList.append(bars)
                    dt = bars[0].date.strftime("%Y%m%d %H:%M:%S")
                    print(f'{output_symbol}: {dt}')
                    allBars = [b for bars in reversed(barsList) for b in bars]
                    df = ib_insync.util.df(allBars)

                    df.to_csv(f'full_{output_symbol}_{what_to_show}_{bar_length.replace(" ", "_")}.csv', index=False)


def update_file(contract, file_name):
    futures = [ib_insync.ContFuture(contract.symbol, contract.exchange) for contract in futures]
    equities = [ib_insync.Stock(contract.symbol, contract.exchange) for contract in equities]
    currencies = [ib_insync.Forex(pair) for pair in currencies]

    bar_length_to_duration = {'1 hour': '5 D', '5 mins': '5 D', '1 min': '5 D'}

    for bar_length in ['1 min', '5 mins', '1 hour']:
        for contracts in [currencies, futures, equities]:
            for contract in contracts:
                print(f'Getting {contract}')
                dt = ''
                barsList = []
                what_to_show = 'MIDPOINT' if contract.exchange == 'IDEALPRO' else 'TRADES'
                output_symbol = contract.pair() if contract.exchange == 'IDEALPRO' else contract.symbol
                bars = ib.reqHistoricalData(
                    contract,
                    endDateTime=dt,
                    durationStr=bar_length_to_duration[bar_length],
                    barSizeSetting=bar_length,
                    whatToShow=what_to_show,
                    useRTH=False,
                    formatDate=2)
                allBars = [b for bars in reversed(barsList) for b in bars]
                df = ib_insync.util.df(allBars)
                csv_location = f'full_{output_symbol}_{what_to_show}_{bar_length.replace(" ", "_")}.csv'
                df.to_csv(csv_location, index=False, mode='a', header=False)
                drop_duplicates_from_csv(csv_location)


if __name__ == '__main__':

    ib = ib_insync.IB()

    ib.connect('127.0.0.1', 7497, clientId=100, readonly=True)
    if not ib.isConnected():
        ib.connect('127.0.0.1', 4002, clientId=100, readonly=True)

    futures = [ib_insync.ContFuture(contract.symbol, contract.exchange) for contract in futures]
    equities = [ib_insync.Stock(contract.symbol, contract.exchange) for contract in equities]
    currencies = [ib_insync.Forex(pair) for pair in currencies]

    bar_lengths = ['1 min', '5 mins', '1 hour']

    fut_inputs = [(contract, f'full_{contract.symbol}_TRADES_{bar_length.replace(" ", "_")}.csv') for contract in
                  futures for bar_length in ['1 min', '5 mins', '1 hour']]

    cur_inputs = [(contract, f'full_{contract.pair()}_MIDPOINT_{bar_length.replace(" ", "_")}.csv') for contract in
                  currencies for bar_length in ['1 min', '1 hour']]

    etf_inputs = [(contract, f'full_{contract.symbol}_TRADES_{bar_length.replace(" ", "_")}.csv') for contract in
                  equities for bar_length in ['1 min', '5 mins', '1 hour']]

    inputs = fut_inputs + cur_inputs + etf_inputs

    for contract, file_name in inputs:
        if exists(file_name):
            print(f'Updating {file_name}')
            update_file(contract, file_name)
        else:
            create_new(contract, file_name)

