Hey Nick, below is a more complete example of how you can write a Python script to:
	1.	Use the yfinance library to fetch ETF data, including:
	•	Historical dividends.
	•	Sector weightings (if available).
	2.	Organize this information in a way that could help you with your portfolio balancing.

Note:
	•	yfinance is a convenient library for pulling stock and ETF data from Yahoo Finance. It doesn’t require an external API key.
	•	Dividend data should be generally available for most ETFs.
	•	Sector weightings are available for many (but not all) ETFs in the info attribute. Some ETFs may not have this info, in which case you’d need to use another API or data source (e.g., Finnhub, Alpha Vantage, or Morningstar APIs) if you have an API key.
	•	The script below defaults to a single ETF symbol, but you can easily loop over a list of ETF symbols to gather data for multiple funds.

Setup:
Install yfinance if you haven’t already:

pip install yfinance

Script Example (etf_data.py):

import yfinance as yf
import pandas as pd
import sys

def get_etf_data(etf_symbol: str):
    """Fetches ETF data including dividends and sector weights from Yahoo Finance."""
    # Download ETF data
    etf = yf.Ticker(etf_symbol)
    
    # Get dividends as a Pandas Series; index = date, values = dividend amount
    dividends = etf.dividends
    
    # Fetch ETF info dictionary (contains metadata and possibly sector weights)
    info = etf.info
    
    # Sector weights are often stored in 'sectorWeightings' or 'sectorWeights' key
    # Exact key can vary. We'll check a few common fields.
    sector_weights = info.get('sectorWeightings', None)
    if sector_weights is None:
        # Some ETFs might store it in 'sectorWeights' or another variation
        # SPDR ETFs often break it down into a dict of sector: weight
        sector_weights = info.get('sectorWeights', None)
    
    # Sector weights from yfinance often come as a list of dicts, e.g.:
    # [{'Technology': 0.20}, {'Healthcare': 0.15}, ...]
    # Let's convert it into a single dict {SectorName: Weight} for convenience.
    structured_sector_weights = {}
    if sector_weights and isinstance(sector_weights, (list, dict)):
        if isinstance(sector_weights, list):
            for sector_dict in sector_weights:
                # Each element in the list is a dict with one key/value
                # e.g. {'Technology': 0.20}
                for sector, weight in sector_dict.items():
                    structured_sector_weights[sector] = weight
        elif isinstance(sector_weights, dict):
            # If it's already a dict, just use it directly
            structured_sector_weights = sector_weights
    
    return dividends, structured_sector_weights

def main():
    # Check for command line arguments: python etf_data.py ETF_SYMBOL
    # If none provided, default to a popular ETF like 'VTI'
    if len(sys.argv) > 1:
        etf_symbol = sys.argv[1]
    else:
        etf_symbol = "VTI"  # Total Stock Market ETF as default
    
    dividends, sector_weights = get_etf_data(etf_symbol)
    
    # Print out dividends
    # Dividends is a Pandas Series with Date index and Dividend amount values
    print(f"--- Dividends for {etf_symbol} ---")
    if dividends.empty:
        print("No dividend data found.")
    else:
        # You can manipulate dividends to find average yield, recent yields, etc.
        print(dividends.tail(10))  # show last 10 dividend entries
    
    # Print out Sector Weights
    print(f"\n--- Sector Weights for {etf_symbol} ---")
    if not sector_weights:
        print("No sector weight data found.")
    else:
        for sector, weight in sector_weights.items():
            # Weight is often a fraction (e.g. 0.20 = 20%)
            print(f"{sector}: {weight * 100:.2f}%")

if __name__ == "__main__":
    main()

How to Use This Script:
	1.	Run the script in your terminal or command prompt:

python etf_data.py VTI

If you don’t provide an ETF symbol, it defaults to “VTI.”

	2.	The script will print out the last 10 dividend payments and the sector allocation breakdown.
	3.	You can integrate the returned data into another function that helps you decide how to rebalance your portfolio. For example, you might:
	•	Compare sector weights across your entire portfolio to ensure you aren’t overly concentrated in a single sector.
	•	Use the dividends data to estimate your expected income and see if you need to adjust your holdings.

Extending the Script:
	•	If you want more granularity or need different data points (like expense ratio, top holdings, etc.), check etf.info printout to see what’s available.
	•	For ETFs that don’t have sector data in info, consider using another data source. With an API key from a service like Finnhub:

import requests

api_key = "YOUR_FINNHUB_API_KEY"
url = f"https://finnhub.io/api/v1/etf/holdings?symbol={etf_symbol}&token={api_key}"
response = requests.get(url)
holdings_data = response.json() 
# Process holdings_data to extract sector info or do calculations.



This should give you a solid starting point, Nick. From here, you can add logic to store results in a CSV file, compare multiple ETFs, or integrate your own logic to help with rebalancing decisions.