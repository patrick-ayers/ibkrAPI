''' Demonstrates how an application can request the current time '''

import ib_insync
import pandas as pd
from contracts import equities, futures, currencies
from os.path import exists


def create_new(contract, bar_length, file_name):
    print(f'Creating {file_name}')
    bar_length_to_duration = {'1 hour': '1 M', '5 mins': '10 D', '1 min': '5 D', '1 day': '1 Y'}

    dt = ''
    barsList = []
    what_to_show = 'MIDPOINT' if contract.exchange == 'IDEALPRO' else 'TRADES'
    if contract.exchange == 'IDEALPRO':
        output_symbol = contract.pair()
    else:
        output_symbol = contract.symbol
    while True:
        bars = ib.reqHistoricalData(
            contract,
            endDateTime=dt,
            durationStr=bar_length_to_duration[bar_length],
            barSizeSetting=bar_length,
            whatToShow=what_to_show,
            useRTH=False,
            formatDate=2)

        if not bars or dt == bars[0].date.strftime("%Y%m%d %H:%M:%S"):
            break
        barsList.append(bars)
        dt = bars[0].date.strftime("%Y%m%d %H:%M:%S")
        print(f'{file_name}: {dt}')
    allBars = [b for bars in reversed(barsList) for b in bars]
    df = ib_insync.util.df(allBars)
    df = df.iloc[::-1]
    df.to_csv(file_name, index=False)


def update_file(contract, bar_length, file_name):
    print(f'Updating {file_name}')

    bar_length_to_duration = {'1 hour': '5 D', '5 mins': '5 D', '1 min': '5 D', '1 day': '5 D'}

    dt = ''
    barsList = []
    what_to_show = 'MIDPOINT' if contract.exchange == 'IDEALPRO' else 'TRADES'
    bars = ib.reqHistoricalData(
        contract,
        endDateTime=dt,
        durationStr=bar_length_to_duration[bar_length],
        barSizeSetting=bar_length,
        whatToShow=what_to_show,
        useRTH=False,
        formatDate=2)
    barsList.append(bars)
    allBars = [b for bars in reversed(barsList) for b in bars]
    new_df = ib_insync.util.df(allBars)

    old_df = pd.read_csv(file_name)

    df = new_df.append(old_df)
    df = df.drop_duplicates(subset=['date'], keep='first')
    df = df.iloc[::-1]

    df.to_csv(file_name)

def refresh_file(contract, bar_length, file_name):
    #TODO write function to 1) pull as much history as possible 2) deduplicate existing file (replacing with new data)
    pass

def refresh_all(contract, bar_length, file_name):
    #TODO Loop over refresh_file()
    pass

if __name__ == '__main__':

    ib = ib_insync.IB()

    ib.connect('127.0.0.1', 4001, clientId=100, readonly=True)
    if not ib.isConnected():
        ib.connect('127.0.0.1', 7497, clientId=100, readonly=True)

    futures = [ib_insync.ContFuture(contract.symbol, contract.exchange) for contract in futures]
    equities = [ib_insync.Stock(contract.symbol, contract.exchange) for contract in equities]
    currencies = [ib_insync.Forex(pair) for pair in currencies]

    fut_inputs = [(contract, bar_length, f'full_{contract.symbol}_TRADES_{bar_length.replace(" ", "_")}.csv') for
                  contract in
                  futures for bar_length in [
                      '1 min',
                      '5 mins',
                      '1 hour',
                      '1 day',
                      '5 mins',
                  ]]

    cur_inputs = [(contract, bar_length, f'full_{contract.pair()}_MIDPOINT_{bar_length.replace(" ", "_")}.csv') for
                  contract in
                  currencies for bar_length in [
                      # '1 min',
                      '1 hour',
                      '1 day'
                  ]]

    etf_inputs = [(contract, bar_length, f'full_{contract.symbol}_TRADES_{bar_length.replace(" ", "_")}.csv') for
                  contract in
                  equities for bar_length in [
                      # '1 min',
                      '1 hour',
                      '1 day'
                  ]]

    data_inputs = fut_inputs + cur_inputs + etf_inputs

    for the_tuple in data_inputs:
        print(the_tuple)
        the_contract, bar_length, file_name = the_tuple
        if exists(file_name):
            #continue  ##TODO fix update
            update_file(the_contract, bar_length, file_name)
        else:
            create_new(the_contract, bar_length, file_name)
