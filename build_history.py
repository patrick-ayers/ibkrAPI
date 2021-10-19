''' Demonstrates how an application can request the current time '''


import ib_insync

def main():
    from contracts import equities, futures
    ib = ib_insync.IB()

    ib.connect('127.0.0.1', 7497, clientId=100, readonly=True)
    if not ib.isConnected():
        ib.connect('127.0.0.1', 4002, clientId=100, readonly=True)

    futures = [ib_insync.ContFuture(contract.symbol, contract.exchange) for contract in futures]
    equities = [ib_insync.Stock(contract.symbol, contract.exchange) for contract in equities]
    for contracts in [futures, equities]:
        for contract in contracts:
            print(f'Getting {contract}')
            dt = ''
            barsList = []
            while True:
                bars = ib.reqHistoricalData(
                    contract,
                    endDateTime=dt,
                    durationStr='10 D',
                    barSizeSetting='5 mins',
                    whatToShow='TRADES',
                    useRTH=False,
                    formatDate=2)
                if not bars:
                    break
                barsList.append(bars)
                dt = bars[0].date.strftime("%Y%m%d %H:%M:%S")
                print(f'{contract.symbol}: {dt}')
            allBars = [b for bars in reversed(barsList) for b in bars]
            df = ib_insync.util.df(allBars)
            df.to_csv(f'full_{contract.symbol}_TRADES_5M.csv', index=False)


if __name__ == '__main__':
    main()
