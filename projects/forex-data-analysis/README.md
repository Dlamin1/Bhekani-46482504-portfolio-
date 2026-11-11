# Forex Historical Data Analysis

An educational Python tool for analysing historical OHLC candles from a CSV file. It calculates simple moving averages, RSI and ATR, then prints a transparent rule-based observation.

## CSV format
Required headers: `timestamp,open,high,low,close`. Example rows are provided in `sample_data.csv`. Use historical data you have permission to use.

## Run
```bash
python -m pip install -r requirements.txt
python analyze.py sample_data.csv --fast 5 --slow 13 --rsi 14
python -m unittest discover -s tests -v
```

## Method
- SMA: arithmetic mean of the most recent N closes.
- RSI: Wilder-style smoothed gain/loss calculation.
- ATR: Wilder-style smoothed true range.
- Observation: compares fast and slow SMA and uses RSI as a filter. It is an educational rule, not a trading recommendation.

## Risk and limitations
This project only reads local historical data. It does not fetch live quotes, connect to a broker, execute orders, account for spread/slippage/fees or predict future returns. Backtests and indicators can mislead; past performance does not guarantee future results.
