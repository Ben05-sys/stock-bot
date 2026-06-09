from scanner import scan_stocks
print("Scanning now...", flush=True)
results = scan_stocks()
if results:
    for s in results:
        print(f"FOUND: {s['symbol']} | Price: {s['price']} | RSI: {s['rsi']} | Vol Ratio: {s['volume_ratio']}", flush=True)
else:
    print("No stocks passed all 4 conditions today.", flush=True)
