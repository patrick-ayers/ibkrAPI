from ibapi.contract import Contract


def get_contract(ticker='MNQ', expiry=None, exchange='GLOBEX', local_symbol=None):
    contract = Contract()
    contract.symbol = ticker
    contract.secType = 'FUT'
    contract.exchange = exchange
    contract.lastTradeDateOrContractMonth = expiry
    contract.localSymbol = local_symbol
    return contract


def get_perp(ticker='MNQ', exchange='GLOBEX'):
    contract = Contract()
    contract.symbol = ticker
    contract.secType = "CONTFUT"
    contract.exchange = exchange
    return contract


def get_equity(ticker='MNQ', exchange='SMART', currency='USD'):
    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.exchange = exchange
    contract.currency = currency
    return contract


def get_fx_pair(cur='EUR', base='USD'):
    contract = Contract()
    contract.symbol = cur
    contract.secType = "CASH"
    contract.currency = base
    contract.exchange = "IDEALPRO"
    return contract


futures = []
equities = []

for x in ['MES', 'MNQ', 'M2K']:
    futures.append(get_perp(x))

for x in ['MYM', 'ZT', 'ZF', 'ZN', 'ZB', 'ZC', 'ZS', ]:
    futures.append(get_perp(x, 'ECBOT'))

for x in ['SI', 'GC', 'HG', 'RB', 'HO', 'CL', 'NG', ]:
    futures.append(get_perp(x, 'NYMEX'))

etfs = ["AMLP",
        #        "ASHR",
        "BKLN",
        "EEM",
        "EFA",
        "EWG",
        "EWH",
        "EWJ",
        "EWT",
        "EWZ",
        "FXI",
        #        "GDX",
        #        "GDXJ",
        #        "GLD",
        "HYG",
        "IAU",
        "IEF",
        "IEFA",
        "IEMG",
        "IVV",
        "IWM",
        "IYR",
        "JNK",
        "KRE",
        "LQD",
        "NUGT",
        #        "OIH",
        "QQQ",
        "RSX",
        "SDS",
        "SH",
        "SLV",
        #        "SMH",
        "SPXL",
        "SPY",
        "SQQQ",
        "TBT",
        "TLT",
        "TQQQ",
        "UPRO",
        "USMV",
        "USO",
        "UVXY",
        "VEA",
        "VWO",
        "VXX",
        "XLB",
        "XLE",
        "XLF",
        "XLI",
        "XLK",
        "XLP",
        "XLRE",
        "XLU",
        "XLV",
        "XOP", ]

exchange = {'ASHR': 'ARCA',
            'GDX': 'ARCA',
            'GDXA': 'ARCA',
            'GLD': 'ARCA',
            'OIH': 'ARCA',
            'SMH': 'NASDAQ'
            }

for x in etfs:
    equities.append(get_equity(x, exchange.setdefault(x, 'SMART')))
