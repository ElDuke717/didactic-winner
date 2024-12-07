import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from config import ALPHA_VANTAGE_API_KEY

class ETFAnalyzer:
    def __init__(self):
        self.api_key = ALPHA_VANTAGE_API_KEY
        self.base_url = "https://www.alphavantage.co/query"

    def get_dividend_history(self, symbol):
        """Fetch dividend history for the ETF"""
        params = {
            "function": "TIME_SERIES_MONTHLY_ADJUSTED",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        if "Monthly Adjusted Time Series" not in data:
            raise Exception("No data found for this symbol")
            
        # Extract dividend data
        dividends = {}
        for date, values in data["Monthly Adjusted Time Series"].items():
            dividend = float(values["7. dividend amount"])
            if dividend > 0:
                dividends[date] = dividend
                
        return dividends

    def plot_dividend_history(self, symbol):
        """Create a visualization of dividend history"""
        dividends = self.get_dividend_history(symbol)
        
        dates = [datetime.strptime(date, "%Y-%m-%d") for date in dividends.keys()]
        values = list(dividends.values())
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, values, marker='o')
        plt.title(f'Dividend History for {symbol}')
        plt.xlabel('Date')
        plt.ylabel('Dividend Amount ($)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return plt

    def get_sector_weights(self, symbol):
        """Fetch sector weights for the ETF"""
        # Note: Alpha Vantage doesn't provide direct sector weights
        # This is a mock implementation - you might need to get this data
        # from another source or manually input it
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        # Mock sector weights (replace with actual data source)
        sector_weights = {
            "Technology": 25.5,
            "Financial Services": 20.3,
            "Healthcare": 15.7,
            "Consumer Cyclical": 12.4,
            "Industrials": 10.2,
            "Consumer Defensive": 7.5,
            "Energy": 4.2,
            "Real Estate": 2.1,
            "Basic Materials": 1.6,
            "Utilities": 0.5
        }
        
        return sector_weights

    def plot_sector_weights(self, symbol):
        """Create a visualization of sector weights"""
        sector_weights = self.get_sector_weights(symbol)
        
        plt.figure(figsize=(10, 8))
        plt.pie(sector_weights.values(), labels=sector_weights.keys(), autopct='%1.1f%%')
        plt.title(f'Sector Weights for {symbol}')
        plt.axis('equal')
        
        return plt

def main():
    # Replace with your Alpha Vantage API key
    analyzer = ETFAnalyzer()
    
    # Example ETF symbol (e.g., SPY for S&P 500 ETF)
    symbol = "VYM"
    
    try:
        # Create dividend history plot
        dividend_plot = analyzer.plot_dividend_history(symbol)
        dividend_plot.savefig(f'{symbol}_dividends.png')
        dividend_plot.close()
        
        # Create sector weights plot
        sector_plot = analyzer.plot_sector_weights(symbol)
        sector_plot.savefig(f'{symbol}_sectors.png')
        sector_plot.close()
        
        print(f"Analysis complete! Check {symbol}_dividends.png and {symbol}_sectors.png")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()