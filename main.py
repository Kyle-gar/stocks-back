from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from strategies.momentum import momentum_signal
from strategies.mean_reversion import mean_reversion_signal
from strategies.ml_predictor import ml_predictor_signal
from utils.data import get_realtime_price, get_historical_data
from utils.risk import position_size, max_drawdown

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AlphaPulse backend is running."}

@app.get("/signal")
def get_signal(
    ticker: str = Query(...),
    interval: str = Query("1m"),
    account_balance: float = Query(10000.0),
    risk_per_trade: float = Query(0.01)
):
    price = get_realtime_price(ticker)
    hist = get_historical_data(ticker, interval)
    results = [
        momentum_signal(hist),
        mean_reversion_signal(hist),
        ml_predictor_signal(hist)
    ]
    # Ensemble: majority vote, weighted by confidence
    votes = {"Buy": 0, "Sell": 0, "Hold": 0}
    for r in results:
        votes[r["signal"]] += r["confidence"]
    signal = max(votes, key=votes.get)
    confidence = votes[signal] / sum(votes.values())
    # Risk management: position sizing
    stop_loss_pct = 0.02  # Example: 2% stop
    size = position_size(account_balance, risk_per_trade, stop_loss_pct)
    return {
        "ticker": ticker.upper(),
        "price": price,
        "signal": signal,
        "confidence": round(confidence, 2),
        "position_size": round(size, 2),
        "details": results
    }
