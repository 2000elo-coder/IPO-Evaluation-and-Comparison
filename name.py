import requests
import pandas as pd

def fetch_india_ipos(status="open", api_key="2b95c350ee4bbb2f6bc0d274089f61d07e05ae0864285830dc0987da27dc2e19"):
    """
    Fetch IPOs in India from IPOAlerts API.
    
    Args:
        status (str): one of "open", "upcoming", "closed", "announced", "listed".
        api_key (str): your API key if required.
    Returns:
        pandas.DataFrame: table of IPOs with fields from API.
    """
    base_url = "https://api.ipoalerts.in/ipos"
    params = {"status": status}
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key  # adjust if API requires header
    resp = requests.get(base_url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # The JSON has a key "ipos" per docs :contentReference[oaicite:6]{index=6}
    ipos = data.get("ipos", [])
    df = pd.DataFrame(ipos)
    return df

if __name__ == "__main__":
    # If you have a key:
    API_KEY = None  # replace if provided
    df_open = fetch_india_ipos(status="open", api_key=API_KEY)
    

    '''
    print(df_open.head())
    # You might also want upcoming
    df_upcoming = fetch_india_ipos(status="upcoming", api_key=API_KEY)
    print("Upcoming IPOs in India:")
    print(df_upcoming.head())
    '''
    print("Open IPOs in India:")
    print(df_open["name"].to_list())




