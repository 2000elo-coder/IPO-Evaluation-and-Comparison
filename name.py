import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_ipos_nse():
    """Fetch both currently open and upcoming IPOs from NSE."""
    url = "https://www.nseindia.com/market-data/all-upcoming-issues-ipo"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    session = requests.Session()
    resp = session.get(url, headers=headers)
    resp.raise_for_status()
    html = resp.text

    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")

    ipo_data = {"Open": pd.DataFrame(), "Upcoming": pd.DataFrame()}
    titles = ["Currently Open IPOs", "Upcoming IPOs"]

    for i, table in enumerate(tables[:2]):  # Usually two tables
        rows = []
        for tr in table.find_all("tr")[1:]:
            td = tr.find_all("td")
            if len(td) >= 5:
                company = td[0].get_text(strip=True)
                issue_type = td[1].get_text(strip=True)
                open_date = td[2].get_text(strip=True)
                close_date = td[3].get_text(strip=True)
                price_band = td[4].get_text(strip=True)
                rows.append({
                    "Company": company,
                    "Issue Type": issue_type,
                    "Open Date": open_date,
                    "Close Date": close_date,
                    "Price Band": price_band
                })
        ipo_data["Open" if i == 0 else "Upcoming"] = pd.DataFrame(rows)

    return ipo_data

if __name__ == "__main__":
    ipos = fetch_ipos_nse()

    # --- Print Open IPOs ---
    print("\n🟢 Currently Open IPOs on NSE:\n")
    if ipos["Open"].empty:
        print("No IPOs are currently open for subscription.\n")
    else:
        for i, row in ipos["Open"].iterrows():
            print(f"{i+1}. {row['Company']}")
            print(f"   Issue Type : {row['Issue Type']}")
            print(f"   Open Date  : {row['Open Date']}")
            print(f"   Close Date : {row['Close Date']}")
            print(f"   Price Band : {row['Price Band']}\n")

    # --- Print Upcoming IPOs ---
    print("\n📅 Upcoming IPOs on NSE:\n")
    if ipos["Upcoming"].empty:
        print("No upcoming IPOs are listed yet.\n")
    else:
        for i, row in ipos["Upcoming"].iterrows():
            print(f"{i+1}. {row['Company']}")
            print(f"   Issue Type : {row['Issue Type']}")
            print(f"   Open Date  : {row['Open Date']}")
            print(f"   Close Date : {row['Close Date']}")
            print(f"   Price Band : {row['Price Band']}\n")
