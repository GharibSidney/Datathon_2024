import requests

def get_fundamental_prediction(ticker, api_key):
    """
    Tells wether a ticker is a good buy according to fundamentals
    """

    # URL for the Alpha Vantage API
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Check if the response is valid
        if "Note" in data:
            print("API call limit reached. Please try again later.")
            return
        
        # Extract relevant financial metrics
        pe_ratio = data.get("PERatio")
        pb_ratio = data.get("PriceToBookRatio")
        dividend_yield = data.get("DividendYield")
        market_cap = data.get("MarketCapitalization")
        
        # Display the fetched information
        print(f"Fundamental Analysis for {ticker}:\n")
        
        return pe_ratio > 10 or pb_ratio > 3 or dividend_yield > 0.03 or market_cap < 100_000_000
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# Example usage
if __name__ == "__main__":
    # ticker_input = input("Enter a stock ticker: ")
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'  # Replace with your Alpha Vantage API key
    get_fundamental_prediction('AAPL', api_key)
