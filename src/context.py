import time

from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount

class Context:

    def __init__(self, config: dict):
        self.trader = XtQuantTrader(config["path"], self._get_session_id())
        self.account = StockAccount(config["account_id"], "STOCK")

    def setup(self):
        self.trader.start()
        res = self.trader.connect()
        if res != 0:
            print('failed to connect to MiniQMT')
            return
        else:
            print('successfully connect to MiniQMT')
        self.trader.subscribe(self.account)

    @staticmethod
    def _get_session_id():
        return int(str(time.time_ns())[-6:])
