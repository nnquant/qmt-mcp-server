import pandas as pd

from mcp.server.fastmcp import FastMCP
from xtquant import xtconstant

from src.context import Context
from src.utils import load_config

MCP_SERVER_NAME = "qmt-mcp-server"
mcp = FastMCP(MCP_SERVER_NAME, port=8001)
cfg = load_config()
ctx = Context(cfg)
ctx.setup()


@mcp.tool()
def query_account_asset():
    """
    查询账户资产

    :return: 账户资产信息，包含资金账户、可用金额、冻结金额、持仓市值、总资产
    """
    account_info = ctx.trader.query_stock_asset(ctx.account)
    result = f"资金账户={account_info.account_id} 可用金额={account_info.cash} 冻结金额={account_info.frozen_cash} 持仓市值={account_info.market_value} 总资产={account_info.total_asset}"
    return result


@mcp.tool()
def query_account_positions():
    """
    查询账户持仓

    :return: 账户持仓信息，包含股票代码、数量、成本价、当前价、盈亏金额、盈亏比例
    """
    positions = ctx.trader.query_stock_positions(ctx.account)
    dct_positions = []
    for p in positions:
        dct_positions.append({
            "股票代码": p.stock_code,
            "数量": p.volume,
            "可用数量": p.can_use_volume,
            "开仓价": p.open_price,
            "市值": p.market_value,
            "冻结数量": p.frozen_volume,
            "在途股份": p.on_road_volume,
            "昨夜拥股": p.yesterday_volume,
            "成本价": p.avg_price
        })
    return pd.DataFrame(dct_positions).to_string()


@mcp.tool()
def create_order(stock_code: str, price: float, quantity: int, side: str):
    """
    创建订单


    :param stock_code: 股票代码 如000001.SZ、600000.SH 注意股票代码需要包含交易所代码SH或SZ
    :param price: 价格
    :param quantity: 数量
    :param side: 方向, buy 或 sell

    :return: 下单成功返回委托编号，下单失败返回-1
    """
    if side == "buy":
        order_type = xtconstant.STOCK_BUY
    elif side == "sell":
        order_type = xtconstant.STOCK_SELL
    else:
        raise NotImplementedError()
    resp = ctx.trader.order_stock(ctx.account, stock_code, order_type, quantity, xtconstant.FIX_PRICE, price, order_remark="mcp")
    if resp < 0:
        return f"下单失败"
    return f"下单成功，委托编号={resp}"


@mcp.tool()
def cancel_order(order_id: int):
    """
    取消订单

    :param order_id: 委托编号

    :return: 撤单结果
    """
    resp = ctx.trader.cancel_order_stock(ctx.account, order_id)
    if resp == 0:
        return f"撤单成功"
    return f"撤单失败"


if __name__ == '__main__':
    mcp.run(transport="sse")
