import schedule
import time
import yfinance as yf
from datetime import datetime
from scanner import scan_stocks
from portfolio import load_portfolio, save_portfolio, buy_stock, sell_stock
from notifier import send_email

TARGET_PROFIT = 0.10   # sell at +10%
STOP_LOSS = -0.05      # sell at -5%


def get_current_price(symbol):
    try:
        df = yf.Ticker(symbol).history(period="1d")
        return round(df["Close"].iloc[-1], 2)
    except Exception:
        return None


def check_exits(portfolio):
    exits = []
    for symbol in list(portfolio["positions"].keys()):
        price = get_current_price(symbol)
        if price is None:
            continue

        buy_price = portfolio["positions"][symbol]["buy_price"]
        change = (price - buy_price) / buy_price

        if change >= TARGET_PROFIT:
            trade = sell_stock(symbol, price, portfolio, "TARGET HIT")
            if trade:
                exits.append(f"SOLD {symbol}: +{trade['profit_pct']}% profit = Rs.{trade['profit']}")

        elif change <= STOP_LOSS:
            trade = sell_stock(symbol, price, portfolio, "STOP LOSS")
            if trade:
                exits.append(f"SOLD {symbol}: {trade['profit_pct']}% stop-loss = Rs.{trade['profit']}")

    return exits


def run_bot():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Running bot...", flush=True)

    portfolio = load_portfolio()
    save_portfolio(portfolio)  # always persist state
    lines = [f"STOCK BOT REPORT - {datetime.now().strftime('%d %b %Y')}"]

    # Check and exit positions
    exits = check_exits(portfolio)
    if exits:
        lines.append("\nEXITS:")
        lines.extend(exits)

    # Buy new stocks if slots available
    if portfolio["cash"] > 500 and len(portfolio["positions"]) < 2:
        lines.append("\nSCANNING FOR STOCKS...")
        good_stocks = scan_stocks()
        already_holding = list(portfolio["positions"].keys())
        new_stocks = [s for s in good_stocks if s["symbol"] not in already_holding]

        if new_stocks:
            for stock in new_stocks[: 2 - len(portfolio["positions"])]:
                shares, cost = buy_stock(stock["symbol"], stock["price"], portfolio)
                if shares:
                    lines.append(f"BOUGHT {stock['symbol']} @ Rs.{stock['price']} x {shares} shares = Rs.{cost}")
        else:
            lines.append("No qualifying stocks found today.")
    else:
        lines.append("\nNo buying today (positions full or low cash).")

    # Live value of open positions
    live_value = portfolio["cash"]
    for sym, pos in portfolio["positions"].items():
        price = get_current_price(sym)
        if price:
            live_value += price * pos["shares"]
        else:
            live_value += pos["cost"]

    growth = round(((live_value - portfolio["initial_capital"]) / portfolio["initial_capital"]) * 100, 2)

    lines.append(f"\nPORTFOLIO SUMMARY:")
    lines.append(f"Cash: Rs.{portfolio['cash']}")
    lines.append(f"Total Value: Rs.{round(live_value, 2)}")
    lines.append(f"Growth: {growth}%")
    lines.append(f"Total Profit: Rs.{portfolio['total_profit']}")

    if portfolio["positions"]:
        lines.append("\nOPEN POSITIONS:")
        for sym, pos in portfolio["positions"].items():
            cur = get_current_price(sym) or pos["buy_price"]
            chg = round(((cur - pos["buy_price"]) / pos["buy_price"]) * 100, 2)
            lines.append(f"  {sym}: {pos['shares']} shares @ Rs.{pos['buy_price']} | Now Rs.{cur} ({chg}%)")

    message = "\n".join(lines)
    print(message)
    send_email(f"Stock Bot — Scan Update {datetime.now().strftime('%d %b %Y')}", message)


if __name__ == "__main__":
    print("Stock Paper Trading Bot Started!")
    print("Capital: Rs.10,000 (virtual)")
    print("Target: +10% per trade | Stop-loss: -5%")
    print("Running first scan now...\n")

    run_bot()

    schedule.every().day.at("10:00").do(run_bot)
    print("\nBot scheduled daily at 10:00 AM.")
    print("Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(60)
