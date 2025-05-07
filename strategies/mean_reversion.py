import numpy as np

def mean_reversion_signal(df):
    if len(df) < 21:
        return {"signal": "Hold", "confidence": 0.5, "strategy": "mean_reversion"}
    sma = df['Close'].rolling(20).mean()
    std = df['Close'].rolling(20).std()
    z = (df['Close'].iloc[-1] - sma.iloc[-1]) / std.iloc[-1]
    if z < -2:
        return {"signal": "Buy", "confidence": 0.85, "strategy": "mean_reversion"}
    elif z > 2:
        return {"signal": "Sell", "confidence": 0.85, "strategy": "mean_reversion"}
    else:
        return {"signal": "Hold", "confidence": 0.5, "strategy": "mean_reversion"}
