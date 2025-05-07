def position_size(account_balance, risk_per_trade, stop_loss_pct):
    # Kelly criterion or fixed fractional position sizing
    risk_amount = account_balance * risk_per_trade
    return risk_amount / stop_loss_pct if stop_loss_pct > 0 else 0

def max_drawdown(equity_curve):
    roll_max = equity_curve.cummax()
    drawdown = (equity_curve - roll_max) / roll_max
    return drawdown.min()
