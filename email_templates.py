from datetime import datetime


def _color(value):
    return "#16a34a" if value >= 0 else "#dc2626"


def _arrow(value):
    return "&#9650;" if value >= 0 else "&#9660;"


def _sign(value):
    return "+" if value >= 0 else ""


def market_report_html(nifty, banknifty, sensex, gainers, losers, advances, declines, sentiment):
    date_str = datetime.now().strftime("%d %B %Y, %I:%M %p")

    sentiment_color = {"BULLISH": "#16a34a", "BEARISH": "#dc2626", "NEUTRAL": "#d97706"}.get(sentiment, "#6b7280")

    def index_row(idx):
        if not idx:
            return "<tr><td colspan='4' style='color:#6b7280;'>Data unavailable</td></tr>"
        c = _color(idx["change"])
        a = _arrow(idx["change"])
        s = _sign(idx["change"])
        return f"""
        <tr>
          <td style='padding:10px 14px;font-weight:600;'>{idx['name']}</td>
          <td style='padding:10px 14px;text-align:right;font-weight:700;'>{idx['current']:,.2f}</td>
          <td style='padding:10px 14px;text-align:right;color:{c};font-weight:600;'>{a} {s}{idx['change']}</td>
          <td style='padding:10px 14px;text-align:right;color:{c};font-weight:600;'>{s}{idx['change_pct']}%</td>
        </tr>"""

    def stock_row(s, is_gainer):
        c = _color(s["change_pct"])
        sign = _sign(s["change_pct"])
        return f"""
        <tr>
          <td style='padding:8px 14px;font-weight:600;'>{s['symbol']}</td>
          <td style='padding:8px 14px;text-align:right;'>Rs. {s['price']:,.2f}</td>
          <td style='padding:8px 14px;text-align:right;color:{c};font-weight:700;'>{sign}{s['change_pct']}%</td>
          <td style='padding:8px 14px;text-align:right;color:{c};'>{sign}Rs. {s['change']}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html>
<head><meta charset='UTF-8'></head>
<body style='margin:0;padding:0;background:#f1f5f9;font-family:Arial,sans-serif;'>
  <table width='100%' cellpadding='0' cellspacing='0' style='background:#f1f5f9;padding:30px 0;'>
    <tr><td align='center'>
      <table width='620' cellpadding='0' cellspacing='0' style='background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);'>

        <!-- Header -->
        <tr>
          <td style='background:linear-gradient(135deg,#1e3a5f,#2563eb);padding:32px 36px;'>
            <div style='color:#93c5fd;font-size:12px;letter-spacing:2px;text-transform:uppercase;'>Paper Trading Bot</div>
            <div style='color:#ffffff;font-size:24px;font-weight:700;margin-top:6px;'>Morning Market Report</div>
            <div style='color:#bfdbfe;font-size:13px;margin-top:4px;'>{date_str}</div>
          </td>
        </tr>

        <!-- Sentiment Badge -->
        <tr>
          <td style='padding:20px 36px 0;'>
            <table cellpadding='0' cellspacing='0'>
              <tr>
                <td style='background:{sentiment_color};color:#fff;padding:6px 18px;border-radius:20px;font-size:13px;font-weight:700;letter-spacing:1px;'>
                  {_arrow(1 if sentiment == "BULLISH" else -1 if sentiment == "BEARISH" else 0)} MARKET SENTIMENT: {sentiment}
                </td>
                <td style='padding-left:14px;color:#6b7280;font-size:13px;'>
                  {advances} Advances &nbsp;|&nbsp; {declines} Declines
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Indices -->
        <tr>
          <td style='padding:24px 36px 0;'>
            <div style='font-size:13px;font-weight:700;color:#6b7280;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>Market Indices</div>
            <table width='100%' cellpadding='0' cellspacing='0' style='border-radius:8px;overflow:hidden;border:1px solid #e2e8f0;'>
              <tr style='background:#f8fafc;'>
                <th style='padding:10px 14px;text-align:left;font-size:12px;color:#64748b;font-weight:600;'>INDEX</th>
                <th style='padding:10px 14px;text-align:right;font-size:12px;color:#64748b;font-weight:600;'>PRICE</th>
                <th style='padding:10px 14px;text-align:right;font-size:12px;color:#64748b;font-weight:600;'>CHANGE</th>
                <th style='padding:10px 14px;text-align:right;font-size:12px;color:#64748b;font-weight:600;'>% CHANGE</th>
              </tr>
              {index_row(nifty)}
              {index_row(banknifty)}
              {index_row(sensex)}
            </table>
          </td>
        </tr>

        <!-- Gainers & Losers -->
        <tr>
          <td style='padding:24px 36px 0;'>
            <table width='100%' cellpadding='0' cellspacing='0'>
              <tr>
                <!-- Gainers -->
                <td width='48%' valign='top'>
                  <div style='font-size:13px;font-weight:700;color:#6b7280;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>Top Gainers</div>
                  <table width='100%' cellpadding='0' cellspacing='0' style='border-radius:8px;overflow:hidden;border:1px solid #dcfce7;'>
                    <tr style='background:#f0fdf4;'>
                      <th style='padding:8px 14px;text-align:left;font-size:11px;color:#16a34a;'>STOCK</th>
                      <th style='padding:8px 14px;text-align:right;font-size:11px;color:#16a34a;'>PRICE</th>
                      <th style='padding:8px 14px;text-align:right;font-size:11px;color:#16a34a;'>GAIN</th>
                    </tr>
                    {''.join(f"<tr><td style='padding:7px 14px;font-weight:600;font-size:13px;'>{s['symbol']}</td><td style='padding:7px 14px;text-align:right;font-size:13px;'>Rs.{s['price']:,.0f}</td><td style='padding:7px 14px;text-align:right;color:#16a34a;font-weight:700;font-size:13px;'>+{s['change_pct']}%</td></tr>" for s in gainers)}
                  </table>
                </td>
                <td width='4%'></td>
                <!-- Losers -->
                <td width='48%' valign='top'>
                  <div style='font-size:13px;font-weight:700;color:#6b7280;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>Top Losers</div>
                  <table width='100%' cellpadding='0' cellspacing='0' style='border-radius:8px;overflow:hidden;border:1px solid #fee2e2;'>
                    <tr style='background:#fef2f2;'>
                      <th style='padding:8px 14px;text-align:left;font-size:11px;color:#dc2626;'>STOCK</th>
                      <th style='padding:8px 14px;text-align:right;font-size:11px;color:#dc2626;'>PRICE</th>
                      <th style='padding:8px 14px;text-align:right;font-size:11px;color:#dc2626;'>LOSS</th>
                    </tr>
                    {''.join(f"<tr><td style='padding:7px 14px;font-weight:600;font-size:13px;'>{s['symbol']}</td><td style='padding:7px 14px;text-align:right;font-size:13px;'>Rs.{s['price']:,.0f}</td><td style='padding:7px 14px;text-align:right;color:#dc2626;font-weight:700;font-size:13px;'>{s['change_pct']}%</td></tr>" for s in losers)}
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Bot Strategy -->
        <tr>
          <td style='padding:24px 36px;'>
            <table width='100%' cellpadding='0' cellspacing='0' style='background:#eff6ff;border-radius:8px;border:1px solid #bfdbfe;'>
              <tr>
                <td style='padding:16px 20px;'>
                  <div style='font-size:13px;font-weight:700;color:#1e40af;margin-bottom:6px;'>BOT STRATEGY TODAY</div>
                  <div style='font-size:13px;color:#1e3a8a;'>Scanning 50 Nifty stocks &nbsp;|&nbsp; Buy: Above MA50 & MA200, RSI 50–70, Volume &gt; 1.5x avg</div>
                  <div style='font-size:13px;color:#1e3a8a;margin-top:4px;'>Target: <strong>+10% profit</strong> per trade &nbsp;|&nbsp; Stop-loss: <strong>-5%</strong></div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style='background:#f8fafc;padding:18px 36px;border-top:1px solid #e2e8f0;text-align:center;'>
            <div style='color:#94a3b8;font-size:12px;'>Auto-generated by Stock Bot &nbsp;|&nbsp; Paper Trading &nbsp;|&nbsp; bensammanuel@gmail.com</div>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def trade_report_html(portfolio, position_details, trades, live_value):
    date_str  = datetime.now().strftime("%d %B %Y, %I:%M %p")
    initial   = portfolio["initial_capital"]
    total_profit = round(portfolio["total_profit"], 2)
    growth_pct   = round(((live_value - initial) / initial) * 100, 2)
    winning   = [t for t in trades if t["profit"] > 0]
    losing    = [t for t in trades if t["profit"] <= 0]
    win_rate  = round((len(winning) / len(trades)) * 100, 1) if trades else 0

    growth_color = _color(growth_pct)

    def stat_card(label, value, color="#1e3a5f"):
        return f"""
        <td style='padding:0 8px;'>
          <table width='130' cellpadding='0' cellspacing='0' style='background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0;'>
            <tr><td style='padding:14px 16px;'>
              <div style='font-size:11px;color:#64748b;font-weight:600;letter-spacing:1px;text-transform:uppercase;'>{label}</div>
              <div style='font-size:18px;font-weight:700;color:{color};margin-top:4px;'>{value}</div>
            </td></tr>
          </table>
        </td>"""

    positions_rows = ""
    if position_details:
        for sym, p in position_details.items():
            c = _color(p["pnl"])
            s = _sign(p["pnl"])
            positions_rows += f"""
            <tr style='border-bottom:1px solid #f1f5f9;'>
              <td style='padding:10px 14px;font-weight:700;'>{sym.replace('.NS','')}</td>
              <td style='padding:10px 14px;text-align:right;'>{p['buy_date']}</td>
              <td style='padding:10px 14px;text-align:right;'>Rs. {p['buy_price']:,.2f}</td>
              <td style='padding:10px 14px;text-align:right;'>Rs. {p['current_price']:,.2f}</td>
              <td style='padding:10px 14px;text-align:right;'>{p['shares']}</td>
              <td style='padding:10px 14px;text-align:right;'>Rs. {p['cost']:,.2f}</td>
              <td style='padding:10px 14px;text-align:right;font-weight:700;color:{c};'>{s}Rs. {p['pnl']} ({s}{p['pnl_pct']}%)</td>
            </tr>"""
    else:
        positions_rows = "<tr><td colspan='7' style='padding:20px;text-align:center;color:#94a3b8;'>No open positions today</td></tr>"

    trade_rows = ""
    if trades:
        for i, t in enumerate(trades, 1):
            c = _color(t["profit"])
            s = _sign(t["profit"])
            reason_color = "#16a34a" if t["reason"] == "TARGET HIT" else "#dc2626"
            trade_rows += f"""
            <tr style='border-bottom:1px solid #f1f5f9;'>
              <td style='padding:10px 14px;font-weight:600;color:#64748b;'>#{i}</td>
              <td style='padding:10px 14px;font-weight:700;'>{t['symbol'].replace('.NS','')}</td>
              <td style='padding:10px 14px;text-align:right;'>{t['buy_date']}</td>
              <td style='padding:10px 14px;text-align:right;'>{t['sell_date']}</td>
              <td style='padding:10px 14px;text-align:right;'>Rs. {t['buy_price']:,.2f}</td>
              <td style='padding:10px 14px;text-align:right;'>Rs. {t['sell_price']:,.2f}</td>
              <td style='padding:10px 14px;text-align:right;font-weight:700;color:{c};'>{s}Rs. {t['profit']} ({s}{t['profit_pct']}%)</td>
              <td style='padding:10px 14px;text-align:center;'>
                <span style='background:{"#dcfce7" if t["reason"]=="TARGET HIT" else "#fee2e2"};color:{reason_color};padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;'>{t['reason']}</span>
              </td>
            </tr>"""
    else:
        trade_rows = "<tr><td colspan='8' style='padding:20px;text-align:center;color:#94a3b8;'>No closed trades yet</td></tr>"

    return f"""<!DOCTYPE html>
<html>
<head><meta charset='UTF-8'></head>
<body style='margin:0;padding:0;background:#f1f5f9;font-family:Arial,sans-serif;'>
  <table width='100%' cellpadding='0' cellspacing='0' style='background:#f1f5f9;padding:30px 0;'>
    <tr><td align='center'>
      <table width='700' cellpadding='0' cellspacing='0' style='background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);'>

        <!-- Header -->
        <tr>
          <td style='background:linear-gradient(135deg,#1e3a5f,#2563eb);padding:32px 36px;'>
            <div style='color:#93c5fd;font-size:12px;letter-spacing:2px;text-transform:uppercase;'>Paper Trading Bot</div>
            <div style='color:#ffffff;font-size:24px;font-weight:700;margin-top:6px;'>Daily Trade Report</div>
            <div style='color:#bfdbfe;font-size:13px;margin-top:4px;'>{date_str}</div>
          </td>
        </tr>

        <!-- Stats Row -->
        <tr>
          <td style='padding:24px 28px 0;'>
            <table cellpadding='0' cellspacing='0'>
              <tr>
                {stat_card("Starting Capital", f"Rs.{initial:,.0f}")}
                {stat_card("Current Value", f"Rs.{live_value:,.0f}")}
                {stat_card("Total P&L", f"{_sign(total_profit)}Rs.{abs(total_profit):,.2f}", _color(total_profit))}
                {stat_card("Growth", f"{_sign(growth_pct)}{growth_pct}%", growth_color)}
                {stat_card("Win Rate", f"{win_rate}%", "#16a34a" if win_rate >= 50 else "#dc2626")}
              </tr>
            </table>
          </td>
        </tr>

        <!-- Open Positions -->
        <tr>
          <td style='padding:24px 36px 0;'>
            <div style='font-size:13px;font-weight:700;color:#6b7280;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>Open Positions</div>
            <table width='100%' cellpadding='0' cellspacing='0' style='border-radius:8px;overflow:hidden;border:1px solid #e2e8f0;font-size:13px;'>
              <tr style='background:#f8fafc;'>
                <th style='padding:10px 14px;text-align:left;font-size:11px;color:#64748b;'>STOCK</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>BUY DATE</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>BUY PRICE</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>CUR PRICE</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>SHARES</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>INVESTED</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>UNREALISED P&L</th>
              </tr>
              {positions_rows}
            </table>
          </td>
        </tr>

        <!-- Trade History -->
        <tr>
          <td style='padding:24px 36px;'>
            <div style='font-size:13px;font-weight:700;color:#6b7280;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>Closed Trade History</div>
            <table width='100%' cellpadding='0' cellspacing='0' style='border-radius:8px;overflow:hidden;border:1px solid #e2e8f0;font-size:13px;'>
              <tr style='background:#f8fafc;'>
                <th style='padding:10px 14px;text-align:left;font-size:11px;color:#64748b;'>#</th>
                <th style='padding:10px 14px;text-align:left;font-size:11px;color:#64748b;'>STOCK</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>BUY DATE</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>SELL DATE</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>BUY PRICE</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>SELL PRICE</th>
                <th style='padding:10px 14px;text-align:right;font-size:11px;color:#64748b;'>P&L</th>
                <th style='padding:10px 14px;text-align:center;font-size:11px;color:#64748b;'>EXIT</th>
              </tr>
              {trade_rows}
            </table>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style='background:#f8fafc;padding:18px 36px;border-top:1px solid #e2e8f0;text-align:center;'>
            <div style='color:#94a3b8;font-size:12px;'>Auto-generated by Stock Bot &nbsp;|&nbsp; Paper Trading &nbsp;|&nbsp; bensammanuel@gmail.com</div>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""
