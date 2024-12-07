import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def analyze_etf(ticker):
    """
    Analyze an ETF's dividends and sector weights.
    
    Parameters:
    ticker (str): ETF ticker symbol
    
    Returns:
    dict: A dictionary containing ETF analysis information
    """
    # Fetch ETF information
    etf = yf.Ticker(ticker)
    info = etf.info

    # Dividend analysis
    dividend_data = {
        'Annual Dividend Rate': info.get('dividendRate', 'N/A'),
        'Dividend Yield': info.get('dividendYield', 'N/A'),
        'Ex-Dividend Date': info.get('exDividendDate', 'N/A')
    }

    # Sector weights retrieval and formatting
    sector_weights = info.get('sectorWeightings', [])
    # sectorWeightings is often a list like: [{'Technology': 0.20}, {'Healthcare': 0.15}, ...]
    sector_dict = {}
    for entry in sector_weights:
        sector_dict.update(entry)

    if sector_dict:
        sector_df = pd.DataFrame(list(sector_dict.items()), columns=['Sector', 'Weight'])
        sector_df = sector_df.sort_values('Weight', ascending=False)
    else:
        sector_df = pd.DataFrame(columns=['Sector', 'Weight'])

    # Visualize sector weights if available
    if not sector_df.empty:
        plt.figure(figsize=(10, 6))
        sector_df.set_index('Sector')['Weight'].plot(kind='bar')
        plt.title(f'{ticker} Sector Weights')
        plt.xlabel('Sectors')
        plt.ylabel('Weight (%)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'{ticker}_sector_weights.png')
        plt.close()
    else:
        print(f"No sector weight data available for {ticker}")

    # Top holdings (if available)
    # There’s no built-in attribute `top_holdings` in yfinance. Check if `info` has something similar.
    holdings = info.get('holdings', [])
    if holdings:
        top_holdings = pd.DataFrame(holdings).head(10)
    else:
        # If this key does not exist or is empty, we return an empty DataFrame
        top_holdings = pd.DataFrame()
    
    return {
        'dividend_info': dividend_data,
        'sector_weights': sector_df,
        'top_holdings': top_holdings
    }

def compare_etfs(tickers):
    """
    Compare multiple ETFs
    
    Parameters:
    tickers (list): List of ETF ticker symbols
    
    Returns:
    DataFrame: Comparison of ETF characteristics
    """
    etf_comparisons = []
    
    for ticker in tickers:
        etf_data = analyze_etf(ticker)
        comparison_entry = {
            'Ticker': ticker,
            'Annual Dividend Rate': etf_data['dividend_info']['Annual Dividend Rate'],
            'Dividend Yield': etf_data['dividend_info']['Dividend Yield']
        }
        etf_comparisons.append(comparison_entry)
    
    return pd.DataFrame(etf_comparisons)

def main():
    # Single ETF analysis
    vti_analysis = analyze_etf('VTI')
    
    # Print dividend information
    print("Dividend Information:")
    for key, value in vti_analysis['dividend_info'].items():
        print(f"{key}: {value}")
    
    # Print sector weights
    print("\nSector Weights:")
    print(vti_analysis['sector_weights'])
    
    # Print top holdings
    print("\nTop Holdings:")
    print(vti_analysis['top_holdings'])
    
    # Compare multiple ETFs
    comparison = compare_etfs(['VTI', 'VOO', 'QQQ'])
    print("\nETF Comparison:")
    print(comparison)

if __name__ == "__main__":
    main()