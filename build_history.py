''' Demonstrates how an application can request the current time '''
from datetime import datetime
from threading import Thread
import time
import pandas as pd
import pytz as tz

from contracts import futures, equities


from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.utils import iswrapper

class SimpleClient(EWrapper, EClient):
    ''' Serves as the client and the wrapper '''

    def __init__(self, addr, port, client_id):
        EClient. __init__(self, self)
        # TODO Add DataFrame capable of recieving historic data
        # Connect to TWS
        self.connect(addr, port, client_id)

        # Launch the client thread
        thread = Thread(target=self.run)
        thread.start()

    @iswrapper
    def error(self, req_id, code, msg):
        print('Error {}: {}'.format(code, msg))

    @iswrapper
    def historicalData(self, reqId, bar):
        ''' Called in response to reqHistoricalData '''
        #TODO Handle export to outside object

        print('historicalData - Close price: {}'.format(bar.close))

def main():
    contracts = futures
    # Create the client and connect to TWS
    client = SimpleClient('127.0.0.1', 7497, 0)

    #TODO Automate to grab most recent Friday
    last_friday_close = datetime.datetime(2021, 10, 15, 19, 00, 00, 0, et)

    prior_fridays = [
        (last_friday_close - datetime.timedelta(n)).strftime("%Y%m%d %H:%M:%S") for n in range(0, 5 * 7, 7)
    ]

    for i in range(len(contracts)):
        for friday in prior_fridays:
            print(f'Getting {name} through {friday}')
            pass
            # TODO implement reqHistoricalData(req_idx, contract, friday, '5 D', '1 min', 'TRADES', 0, 2, False, [])

        #TODO Concatenate weeks of data, save to CSV

    # Disconnect from TWS
    client.disconnect()

if __name__ == '__main__':
    main()

