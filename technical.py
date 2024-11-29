from alpha_vantage.timeseries import TimeSeries
import ta
import pandas as pd

def get_rsi(df):
    print(df)
    df = df['close'].rename('Close').to_frame()

    df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

    latest = df.iloc[-1]
    return latest['rsi'] < 50

def get_macd(df):
    df.columns = ['open', 'high', 'low', 'close', 'volume']

    df['macd'] = ta.trend.MACD(df['close']).macd()
    df['macd_signal'] = ta.trend.MACD(df['close']).macd_signal()
    df['macd_diff'] = ta.trend.MACD(df['close']).macd_diff()

    latest = df.iloc[-1]
    return latest['macd'] > latest['macd_signal']

# def get_stochastic(df):
#     df.columns = ['open', 'high', 'low', 'close', 'volume']

#     stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'], window=14, smooth_window=3)
#     df['stoch_k'] = stoch.stoch()
#     df['stoch_d'] = stoch.stoch_signal()

#     latest = df.iloc[-1]
#     return (latest['stoch_k'] < 20) and (latest['stoch_k'] > latest['stoch_d'])

def get_prediction(ticker):
    """
    Tells you whether you should buy the stock
    """
    api_key = 'YOUR_API_KEY'
    ts = TimeSeries(key=api_key, output_format='pandas')
    df, _ = ts.get_daily(symbol=ticker, outputsize='compact')
    # return int(get_macd(df)) + int(get_rsi(df)) + int(get_stochastic(df)) >= 2
    return int(get_macd(df)) + int(get_rsi(df)) >= 1

if __name__ == '__main__':
    ticker = 'AAPL'
    print(get_prediction(ticker))
