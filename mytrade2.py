import time
import pyupbit
import datetime
import pandas

access = ""
secret = ""


def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups<0] = 0
    downs[downs>0]=0

    AU = ups.ewm(com=period-1, min_periods=period).mean()
    AD = downs.abs().ewm(com=period-1,min_periods=period).mean()
    RS = AU/AD

    return pandas.Series(100-(100/(1+RS)), name="RSI")

# 로그인
upbit = pyupbit.Upbit(access, secret)
coin = ""
print("autotrade start")

buy_position = True
sell_position = False

# 자동매매 시작
while True:
    data = pyupbit.get_ohlcv(ticker=coin,interval="minute3")
    RSI = rsi(data,14).iloc[-1]
    try:
        if buy_position and RSI <= 30:
            krw = get_balance(coin)
            if krw > 5000:
                upbit.buy_market_order(coin, krw*0.9995)
            sell_position = True
                

        elif sell_position and RSI > 63:
            stock = get_balance(coin[4:])
            if stock > 0.00008:
                upbit.sell_market_order(coin, stock*0.9995)
            buy_position = True
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
