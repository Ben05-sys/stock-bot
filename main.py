import schedule
import time
import yfinance as yf
from datetime import datetime
from scanner import scan_stocks
from portfolio import load_portfolio, save_portfolio, buy_stock, sell_stock
from notifier import send_email

STOP_LOSS_ATR    = 1.5   # stop = buy_price - 1.5x ATR
TARGET_ATR       = 3.0   # target = buy_price + 3x ATR (1:2 risk:reward)
BREAKEVEN_ATR    = 1.5   # once price gains 1.5x ATR, move stop to breakeven

# Legacy fallback for positions opened before the ATR-based system existed
LEGACY_STOP_PCT   = -0.05
LEGACY_TARGET_PCT = 0.10


def get_current_price(symbol):
    try:
        df = yf.Ticker(symbol).history(period="1d")
        return round(df["Close"].iloc[-1], 2)
    except Exception:
        return None


def _migrate_legacy_position(pos):
    """Backfill stop_loss/target/atr for positions opened before this system existed."""
    if pos.get("stop_loss") is None:
        pos["stop_loss"] = round(pos["buy_price"] * (1 + LEGACY_STOP_PCT), 2)
    if pos.get("target") is None:
        pos["target"] = round(pos["buy_price"] * (1 + LEGACY_TARGET_PCT), 2)
    pos.setdefault("atr", None)


def check_exits(portfolio):
    exits = []
    for symbol in list(portfolio["positions"].keys()):
        price = get_current_price(symbol)
        if price is None:
            continue

        pos = portfolio["positions"][symbol]
        _migrate_legacy_position(pos)
        buy_price = pos["buy_price"]
        atr = pos["atr"]

        if price <= pos["stop_loss"]:
            trade = sell_stock(symbol, price, portfolio, "STOP LOSS")
            if trade:
                exits.append(f"SOLD {symbol}: {trade['profit_pct']}% stop-loss = Rs.{trade['profit']}")
            continue

        if price >= pos["target"]:
            trade = sell_stock(symbol, price, portfolio, "TARGET HIT")
            if trade:
                exits.append(f"SOLD {symbol}: +{trade['profit_pct']}% profit = Rs.{trade['profit']}")
            continue

        # Trailing stop: once price has gained 1.5x ATR, lock in breakeven
        if atr and pos["stop_loss"] < buy_price and price >= buy_price + BREAKEVEN_ATR * atr:
            pos["stop_loss"] = buy_price
            save_portfolio(portfolio)

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
                stop_loss = round(stock["price"] - STOP_LOSS_ATR * stock["atr"], 2)
                target    = round(stock["price"] + TARGET_ATR * stock["atr"], 2)
                shares, cost = buy_stock(
                    stock["symbol"], stock["price"], portfolio,
                    stop_loss=stop_loss, target=target, atr=stock["atr"],
                )
                if shares:
                    lines.append(
                        f"BOUGHT {stock['symbol']} @ Rs.{stock['price']} x {shares} shares = Rs.{cost} "
                        f"(RS={stock['rel_strength']}% | Stop: Rs.{stop_loss} | Target: Rs.{target})"
                    )
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
    print("Strategy: Relative-strength momentum (uptrend + RSI + volume, ranked vs Nifty 50)")
    print("Risk: ATR-based stop-loss/target (1:2 risk:reward) with breakeven trailing stop")
    print("Running first scan now...\n")

    run_bot()

    schedule.every().day.at("10:00").do(run_bot)
    print("\nBot scheduled daily at 10:00 AM.")
    print("Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(60)
