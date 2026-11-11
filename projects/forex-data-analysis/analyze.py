"""Analyse historical OHLC CSV data with SMA, RSI and ATR indicators."""
import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Candle:
    timestamp: str
    open: float
    high: float
    low: float
    close: float

def load_candles(path):
    candles = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp", "open", "high", "low", "close"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain timestamp,open,high,low,close headers")
        for line, row in enumerate(reader, start=2):
            try:
                candle = Candle(row["timestamp"], *(float(row[key]) for key in ("open", "high", "low", "close")))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid numeric OHLC value on line {line}") from exc
            if candle.high < max(candle.open, candle.close, candle.low) or candle.low > min(candle.open, candle.close, candle.high):
                raise ValueError(f"Inconsistent OHLC values on line {line}")
            candles.append(candle)
    if not candles:
        raise ValueError("CSV contains no candle rows")
    return candles

def sma(values, period):
    if period < 1: raise ValueError("period must be positive")
    if len(values) < period: return None
    return sum(values[-period:]) / period

def rsi(closes, period=14):
    if period < 1: raise ValueError("period must be positive")
    if len(closes) <= period: return None
    changes = [b - a for a, b in zip(closes, closes[1:])]
    gains = [max(change, 0) for change in changes[:period]]
    losses = [max(-change, 0) for change in changes[:period]]
    avg_gain, avg_loss = sum(gains) / period, sum(losses) / period
    for change in changes[period:]:
        avg_gain = (avg_gain * (period - 1) + max(change, 0)) / period
        avg_loss = (avg_loss * (period - 1) + max(-change, 0)) / period
    if avg_loss == 0: return 100.0 if avg_gain else 50.0
    return 100 - (100 / (1 + avg_gain / avg_loss))

def atr(candles, period=14):
    if period < 1: raise ValueError("period must be positive")
    if len(candles) < period + 1: return None
    ranges = []
    for previous, current in zip(candles, candles[1:]):
        ranges.append(max(current.high-current.low, abs(current.high-previous.close), abs(current.low-previous.close)))
    value = sum(ranges[:period]) / period
    for current in ranges[period:]: value = (value * (period - 1) + current) / period
    return value

def analyse(candles, fast=5, slow=13, rsi_period=14):
    closes = [c.close for c in candles]
    fast_value, slow_value = sma(closes, fast), sma(closes, slow)
    momentum = rsi(closes, rsi_period)
    volatility = atr(candles, rsi_period)
    if fast_value is None or slow_value is None:
        observation = "Insufficient data for the selected moving-average periods."
    elif fast_value > slow_value and (momentum is None or momentum >= 50):
        observation = "Bullish momentum condition (historical indicator rule only)."
    elif fast_value < slow_value and (momentum is None or momentum <= 50):
        observation = "Bearish momentum condition (historical indicator rule only)."
    else:
        observation = "Mixed or neutral conditions; no directional observation."
    return {"candles": len(candles), "last_close": closes[-1], "fast_sma": fast_value,
            "slow_sma": slow_value, "rsi": momentum, "atr": volatility, "observation": observation}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    parser.add_argument("--fast", type=int, default=5)
    parser.add_argument("--slow", type=int, default=13)
    parser.add_argument("--rsi", type=int, default=14)
    args = parser.parse_args()
    if min(args.fast, args.slow, args.rsi) < 1: parser.error("periods must be positive")
    try: result = analyse(load_candles(args.csv_file), args.fast, args.slow, args.rsi)
    except (OSError, ValueError) as error: parser.error(str(error))
    for key, value in result.items(): print(f"{key.replace('_', ' ').title():18}: {value if value is not None else 'not enough data'}")

if __name__ == "__main__": main()
