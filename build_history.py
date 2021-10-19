''' Demonstrates how an application can request the current time '''
import datetime
from threading import Thread
import time
import pandas as pd
import pytz as tz

from contracts import futures, equities

import ib_insync

empty_df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'avg', 'vol'])



def main():
    contracts = futures


    # TODO Automate to grab most recent Friday
    last_friday_close = datetime.datetime(2021, 10, 15, 23, 00, 00, 0)

    prior_fridays = [
        (last_friday_close - datetime.timedelta(n)).strftime("%Y%m%d %H:%M:%S") for n in range(0, 50  * 7, 7)
    ]
    req_idx = 0
    for contract in contracts:
        output = empty_df.copy()
        ib = ib_insync.IB()
        ib.connect(readonly=True)
        ib.qualifyContracts(contract)

        for friday in prior_fridays:
            try:
                output.append(util.df(ib.reqHistoricalData(
                    contract,
                    friday,
                    barSizeSetting='1 min',
                    durationStr='5 D',
                    whatToShow='TRADES',
                    useRTH=useRTH,
                    formatDate=2
                )))
                time.sleep(10)  # sleep to allow enough time for data to be returned
            except:
                pass
    # Disconnect from TWS
    client.disconnect()


if __name__ == '__main__':
    main()
