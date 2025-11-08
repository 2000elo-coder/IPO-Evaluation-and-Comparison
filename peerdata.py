import yfinance as yf
import pandas as pd

ticker = "TCS.NS"
t = yf.Ticker(ticker)

# === Updated attributes ===
income = t.income_stmt
balance = t.balance_sheet

# --- Helper function ---
def get_value(df, possible_labels):
    for label in possible_labels:
        if label in df.index:
            return df.loc[label].iloc[0]
    return None  # Return None if not found

# --- Extract financial data based on YOUR row names ---
net_profit = get_value(income, ["Net Income", "Net Income Common Stockholders", "Net Income Common Stockholders", "Net Income Including Noncontrolling Interests"])
revenue = get_value(income, ["Total Revenue", "Operating Revenue"])
equity = get_value(balance, ["Stockholders Equity", "Common Stock Equity", "Total Equity Gross Minority Interest"])
assets = get_value(balance, ["Total Assets"])
debt = get_value(balance, ["Total Debt"])

# --- Info dictionary for market values ---
info = t.info
price = info.get("currentPrice")
eps = info.get("trailingEps")
book_value_per_share = info.get("bookValue")

# --- Compute ratios ---
if all(v is not None for v in [net_profit, revenue, equity, assets]):
    NPM = net_profit / revenue
    ROE = net_profit / equity
    ROA = net_profit / assets
    DE = debt / equity if equity else None
    PE = price / eps if eps and eps != 0 else None
    PB = price / book_value_per_share if book_value_per_share else None

    print(f"\n📊 --- Financial Ratios for {ticker} ---")
    print(f"Net Profit Margin (NPM): {NPM:.2%}")
    print(f"Return on Equity (ROE): {ROE:.2%}")
    print(f"Return on Assets (ROA): {ROA:.2%}")
    print(f"Debt-to-Equity (D/E): {DE:.2f}")
    print(f"P/E Ratio: {PE:.2f}")
    print(f"P/B Ratio: {PB:.2f}")

else:
    print("⚠️ Some key metrics missing for this company.")
