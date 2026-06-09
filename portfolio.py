import json
import os
from datetime import datetime

PORTFOLIO_FILE = "portfolio.json"
INITIAL_CAPITAL = 10000.0


def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        return {
            "cash": INITIAL_CAPITAL,
            "initial_capital": INITIAL_CAPITAL,
            "positions": {},
            "trades": [],
            "total_profit": 0.0,
        }
    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)


def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)


def buy_stock(symbol, price, portfolio):
    slots_left = 2 - len(portfolio["positions"])
    if slots_left <= 0:
        return None, "Max 2 positions already held"

    amount = portfolio["cash"] / slots_left * 0.95
    if amount < 100:
        return None, "Insufficient cash"

    shares = int(amount / price)
    if shares == 0:
        return None, "Not enough cash for 1 share"

    cost = round(shares * price, 2)
    portfolio["cash"] = round(portfolio["cash"] - cost, 2)
    portfolio["positions"][symbol] = {
        "shares": shares,
        "buy_price": round(price, 2),
        "cost": cost,
        "buy_date": datetime.now().strftime("%Y-%m-%d"),
    }
    save_portfolio(portfolio)
    return shares, cost


def sell_stock(symbol, price, portfolio, reason):
    if symbol not in portfolio["positions"]:
        return None

    pos = portfolio["positions"][symbol]
    revenue = round(pos["shares"] * price, 2)
    profit = round(revenue - pos["cost"], 2)
    profit_pct = round((profit / pos["cost"]) * 100, 2)

    portfolio["cash"] = round(portfolio["cash"] + revenue, 2)
    portfolio["total_profit"] = round(portfolio["total_profit"] + profit, 2)

    trade = {
        "symbol": symbol,
        "buy_price": pos["buy_price"],
        "sell_price": round(price, 2),
        "shares": pos["shares"],
        "profit": profit,
        "profit_pct": profit_pct,
        "buy_date": pos["buy_date"],
        "sell_date": datetime.now().strftime("%Y-%m-%d"),
        "reason": reason,
    }
    portfolio["trades"].append(trade)
    del portfolio["positions"][symbol]
    save_portfolio(portfolio)
    return trade
