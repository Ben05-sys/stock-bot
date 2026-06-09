import yfinance as yf
import pandas as pd

STOCKS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS",
    "ICICIBANK.NS", "SBIN.NS", "BAJFINANCE.NS", "HINDUNILVR.NS",
    "AXISBANK.NS", "MARUTI.NS", "TITAN.NS", "ASIANPAINT.NS",
    "KOTAKBANK.NS", "LT.NS", "BHARTIARTL.NS"
]

def calc_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

print(f"{'STOCK':<16} {'PRICE':>8} {'MA50':>8} {'ABVMA50':>8} {'RSI':>6} {'VOLRATIO':>9} {'PASS':>6}")
print("-" * 70)

for symbol in STOCKS:
    try:
        df = yf.Ticker(symbol).history(period="1y", timeout=8)
        df = df.dropna()
        if len(df) < 50:
            continue

        df["MA50"]   = df["Close"].rolling(50).mean()
        df["RSI"]    = calc_rsi(df["Close"])
        df["AvgVol"] = df["Volume"].rolling(20).mean()

        r = df.iloc[-1]
        price     = round(r["Close"], 1)
        ma50      = round(r["MA50"], 1)
        above_ma50 = price > ma50
        rsi       = round(r["RSI"], 1)
        vol_ratio = round(r["Volume"] / r["AvgVol"], 2)
        rsi_ok    = 45 <= rsi <= 75
        vol_ok    = vol_ratio >= 1.2
        passed    = above_ma50 and rsi_ok and vol_ok

        print(f"{symbol.replace('.NS',''):<16} {price:>8} {ma50:>8} {str(above_ma50):>8} {rsi:>6} {vol_ratio:>9} {'YES' if passed else 'NO':>6}")
    except Exception as e:
        print(f"{symbol:<16} ERROR: {e}")
