import yfinance as yf
import pandas as pd

STOCKS = [
    # Nifty 50
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "ICICIBANK.NS", "KOTAKBANK.NS", "BHARTIARTL.NS", "ITC.NS", "SBIN.NS",
    "BAJFINANCE.NS", "LT.NS", "ASIANPAINT.NS", "AXISBANK.NS", "MARUTI.NS",
    "SUNPHARMA.NS", "WIPRO.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "TITAN.NS",
    "TECHM.NS", "POWERGRID.NS", "ONGC.NS", "NTPC.NS", "BAJAJFINSV.NS",
    "HCLTECH.NS", "GRASIM.NS", "DIVISLAB.NS", "JSWSTEEL.NS", "HINDALCO.NS",
    "TATASTEEL.NS", "TATACONSUM.NS", "ADANIPORTS.NS", "COALINDIA.NS", "DRREDDY.NS",
    "CIPLA.NS", "BRITANNIA.NS", "EICHERMOT.NS", "APOLLOHOSP.NS", "BAJAJ-AUTO.NS",
    "HEROMOTOCO.NS", "INDUSINDBK.NS", "SBILIFE.NS", "HDFCLIFE.NS",
    "M&M.NS", "BPCL.NS", "TATAMOTORS.NS", "SHREECEM.NS", "VEDL.NS", "HDFCAMC.NS",
    # Nifty Next 50
    "ADANIENT.NS", "ADANIGREEN.NS", "ADANITRANS.NS", "AMBUJACEM.NS", "BANDHANBNK.NS",
    "BANKBARODA.NS", "BERGEPAINT.NS", "BOSCHLTD.NS", "CANBK.NS", "CHOLAFIN.NS",
    "COLPAL.NS", "DABUR.NS", "DLF.NS", "FEDERALBNK.NS", "GAIL.NS",
    "GODREJCP.NS", "GODREJPROP.NS", "HAVELLS.NS", "ICICIPRULI.NS", "IDEA.NS",
    "IDFCFIRSTB.NS", "IGL.NS", "INDIGO.NS", "IOC.NS", "IRCTC.NS",
    "JUBLFOOD.NS", "LICI.NS", "LUPIN.NS", "MARICO.NS", "MCDOWELL-N.NS",
    "MPHASIS.NS", "MRF.NS", "NAUKRI.NS", "NMDC.NS", "OFSS.NS",
    "PAGEIND.NS", "PEL.NS", "PETRONET.NS", "PFC.NS", "PIDILITIND.NS",
    "PIIND.NS", "PNB.NS", "RECLTD.NS", "SAIL.NS", "SIEMENS.NS",
    "SRF.NS", "TORNTPHARM.NS", "TRENT.NS", "UBL.NS", "ZYDUSLIFE.NS",
    # Nifty Midcap
    "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS", "APLLTD.NS", "ASTRAL.NS",
    "AUBANK.NS", "AUROPHARMA.NS", "BALKRISIND.NS", "BATAINDIA.NS", "BHEL.NS",
    "BIOCON.NS", "COFORGE.NS", "CONCOR.NS", "CROMPTON.NS", "CUMMINSIND.NS",
    "DEEPAKNTR.NS", "ESCORTS.NS", "GMRINFRA.NS", "GNFC.NS", "GRANULES.NS",
    "GSPL.NS", "HDFCAMC.NS", "HINDPETRO.NS", "HONAUT.NS", "IPCALAB.NS",
    "JKCEMENT.NS", "JUBLINGREA.NS", "KAJARIACER.NS", "LALPATHLAB.NS", "LICHSGFIN.NS",
    "LTTS.NS", "MANAPPURAM.NS", "MAPMYINDIA.NS", "MAXHEALTH.NS", "MCX.NS",
    "METROPOLIS.NS", "MFSL.NS", "MOTHERSON.NS", "MUTHOOTFIN.NS", "NAM-INDIA.NS",
    "NATIONALUM.NS", "NAVINFLUOR.NS", "OBEROIRLTY.NS", "PERSISTENT.NS", "PETRONET.NS",
    "POLYCAB.NS", "RBLBANK.NS", "SCHAEFFLER.NS", "SONACOMS.NS", "STARHEALTH.NS",
    "SUNDRMFAST.NS", "SUPREMEIND.NS", "SYNGENE.NS", "THERMAX.NS", "TIMKEN.NS",
    "TTKPRESTIG.NS", "UNIONBANK.NS", "VOLTAS.NS", "WHIRLPOOL.NS", "ZOMATO.NS",
    # Additional Large/Mid caps
    "AARTIIND.NS", "ABBOTINDIA.NS", "ACC.NS", "AFFLE.NS", "AIAENG.NS",
    "AJANTPHARM.NS", "ANGELONE.NS", "ANURAS.NS", "APLLTD.NS", "ATGL.NS",
    "AWFIS.NS", "BAYERCROP.NS", "BLUEDART.NS", "BSOFT.NS", "CANFINHOME.NS",
    "CARBORUNIV.NS", "CDSL.NS", "CEATLTD.NS", "CENTURYPLY.NS", "CHAMBLFERT.NS",
    "CLEAN.NS", "COCHINSHIP.NS", "CREDITACC.NS", "CYIENT.NS", "DATAPATTNS.NS",
    "DELHIVERY.NS", "EDELWEISS.NS", "ELECON.NS", "ELGIEQUIP.NS", "EMAMILTD.NS",
    "ENDURANCE.NS", "EQUITASBNK.NS", "EXIDEIND.NS", "FINEORG.NS", "FLUOROCHEM.NS",
    "GESHIP.NS", "GILLETTE.NS", "GLENMARK.NS", "GLOSTERLTD.NS", "GRINDWELL.NS",
    "HSCL.NS", "IBREALEST.NS", "IDFC.NS", "IIFL.NS", "INDIANB.NS",
    "INDIAMART.NS", "INDRAPRASTHA.NS", "INFIBEAM.NS", "INTELLECT.NS", "IOLCP.NS",
    "JBCHEPHARM.NS", "JKPAPER.NS", "JSWENERGY.NS", "JUSTDIAL.NS", "KPITTECH.NS",
    "KRBL.NS", "KSCL.NS", "LATENTVIEW.NS", "LINDEINDIA.NS", "LUXIND.NS",
    "MAHSEAMLES.NS", "NATCOPHARM.NS", "NIACL.NS", "NIFTYIT.NS", "NLCINDIA.NS",
    "NUVOCO.NS", "OLECTRA.NS", "PGHH.NS", "PHOENIXLTD.NS", "POLYMED.NS",
    "POONAWALLA.NS", "PRINCEPIPE.NS", "PRSMJOHNSN.NS", "QUESS.NS", "RADICO.NS",
    "RAILTEL.NS", "RAJESHEXPO.NS", "RAMCOCEM.NS", "RESPONIND.NS", "RITES.NS",
    "ROUTE.NS", "SANOFI.NS", "SAPPHIRE.NS", "SEQUENT.NS", "SHYAMMETL.NS",
    "SJVN.NS", "SKFINDIA.NS", "SOBHA.NS", "SOLARINDS.NS", "SPANDANA.NS",
    "STLTECH.NS", "SUDARSCHEM.NS", "SUMICHEM.NS", "SUNTV.NS", "SUZLON.NS",
    "SYMPHONY.NS", "TANLA.NS", "TATACOMM.NS", "TATAELXSI.NS", "TATAINVEST.NS",
    "TBOTEK.NS", "TCNSBRANDS.NS", "TEAMLEASE.NS", "TIINDIA.NS", "TIMETECHNO.NS",
    "TORNTPOWER.NS", "TRIL.NS", "TRITURBINE.NS", "UCOBANK.NS", "UJJIVANSFB.NS",
    "UTIAMC.NS", "VAIBHAVGBL.NS", "VGUARD.NS", "VHL.NS", "VINATIORGA.NS",
    "VIPIND.NS", "VMART.NS", "VSTIND.NS", "WELCORP.NS", "WESTAGRI.NS",
    "WOCKPHARMA.NS", "YATHARTH.NS", "ZEEL.NS", "ZENTEC.NS", "ZENSARTECH.NS",
]


NIFTY_INDEX = "^NSEI"


def calc_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calc_atr(df, period=14):
    high, low, close = df["High"], df["Low"], df["Close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def _nifty_return_63d():
    """63-trading-day (~3 month) return of the Nifty 50, used as the benchmark for relative strength."""
    try:
        df = yf.Ticker(NIFTY_INDEX).history(period="1y", timeout=8).dropna()
        if len(df) < 66:
            return 0.0
        return (df["Close"].iloc[-2] / df["Close"].iloc[-65] - 1) * 100
    except Exception:
        return 0.0


def scan_stocks():
    """
    Relative-strength momentum scan:
      1. Trend filter:  Close > MA50 > MA200 (confirmed uptrend, not a short bounce)
      2. Momentum filter: RSI(14) between 45-70 (has momentum, not overbought)
      3. Volume filter: today's volume > 1.2x its 20-day average (real interest, not noise)
      4. Ranking: among stocks passing all filters, rank by 63-day return minus the
         Nifty 50's 63-day return — only buy stocks actually beating the index.
    Each pick also carries its ATR(14), used by main.py to size stop-loss/target
    to that stock's own volatility instead of a fixed percentage.
    """
    nifty_return = _nifty_return_63d()
    candidates = []

    for symbol in STOCKS:
        print(f"  Checking {symbol}...", flush=True)
        try:
            df = yf.Ticker(symbol).history(period="1y", timeout=8).dropna()
            if len(df) < 210:
                continue

            df["MA50"]     = df["Close"].rolling(50).mean()
            df["MA200"]    = df["Close"].rolling(200).mean()
            df["RSI"]      = calc_rsi(df["Close"])
            df["ATR"]      = calc_atr(df)
            df["VolAvg20"] = df["Volume"].rolling(20).mean()

            # Use previous completed day for conditions (avoid partial today data)
            prev = df.iloc[-2]
            cur  = df.iloc[-1]

            price     = prev["Close"]
            uptrend   = price > prev["MA50"] > prev["MA200"]
            rsi       = prev["RSI"]
            rsi_ok    = 45 <= rsi <= 70
            volume_ok = prev["Volume"] > 1.2 * prev["VolAvg20"]

            if not (uptrend and rsi_ok and volume_ok):
                continue

            stock_return = (price / df["Close"].iloc[-65] - 1) * 100
            rel_strength = round(stock_return - nifty_return, 2)
            atr          = round(prev["ATR"], 2)

            candidates.append({
                "symbol":       symbol,
                "price":        round(cur["Close"], 2),   # buy at today's price
                "rsi":          round(rsi, 2),
                "rel_strength": rel_strength,
                "atr":          atr,
                "prev_close":   round(price, 2),
            })
            print(f"  PASS: {symbol} RS={rel_strength}% RSI={round(rsi,1)} ATR={atr}", flush=True)

        except Exception as e:
            print(f"  SKIP {symbol}: {e}", flush=True)
            continue

    # Rank by relative strength vs Nifty 50 — strongest outperformers first
    candidates.sort(key=lambda x: x["rel_strength"], reverse=True)
    return candidates[:2]
