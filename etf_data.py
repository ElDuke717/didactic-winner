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