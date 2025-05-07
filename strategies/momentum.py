import ta

def momentum_signal(df):
    if len(df) < 20:
        return {"signal": "Hold", "confidence": 0.5, "strategy": "momentum"}
    df = df.copy()
    df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['macd'] = ta.trend.MACD(df['Close']).macd_diff()
    rsi = df['rsi'].iloc[-1]
    macd = df['macd'].iloc[-1]
    if rsi > 70 and macd < 0:
        return {"signal": "Sell", "confidence": 0.8, "strategy": "momentum"}
    elif rsi < 30 and macd > 0:
        return {"signal": "Buy", "confidence": 0.8, "strategy": "momentum"}
    else:
        return {"signal": "Hold", "confidence": 0.5, "strategy": "momentum"}
