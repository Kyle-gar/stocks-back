import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

def ml_predictor_signal(df):
    if len(df) < 50:
        return {"signal": "Hold", "confidence": 0.5, "strategy": "ml"}
    # Features: last 20 returns, RSI, MACD
    X = []
    for i in range(30, len(df)):
        returns = df['Close'].pct_change().fillna(0).values[i-20:i]
        rsi = df['Close'].rolling(14).apply(lambda x: (x.diff().clip(lower=0).sum() / abs(x.diff()).sum())*100 if abs(x.diff()).sum() > 0 else 50).iloc[i]
        macd = df['Close'].ewm(span=12).mean().iloc[i] - df['Close'].ewm(span=26).mean().iloc[i]
        X.append(np.concatenate([returns, [rsi, macd]]))
    X = np.array(X)
    y = (df['Close'].shift(-1).iloc[30:len(df)-1] > df['Close'].iloc[30:len(df)-1]).astype(int)
    if len(X) < 10:
        return {"signal": "Hold", "confidence": 0.5, "strategy": "ml"}
    model = GradientBoostingClassifier().fit(X[:-1], y[:-1])
    pred = model.predict(X[-1].reshape(1, -1))[0]
    conf = model.predict_proba(X[-1].reshape(1, -1))[0][pred]
    if pred == 1:
        return {"signal": "Buy", "confidence": float(conf), "strategy": "ml"}
    else:
        return {"signal": "Sell", "confidence": float(conf), "strategy": "ml"}
