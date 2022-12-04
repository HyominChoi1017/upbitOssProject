from dataPrepare import prepareData

def act():
    ppd = prepareData()
    df = ppd[11:][['close', 'RSI']]
    df['daily_rev'] = df['close'].pct_change() + 1

    BUY_THRESHOLD = 20
    SELL_THRESHOLD = 75

    df.loc[df['RSI'] < BUY_THRESHOLD, 'signal'] = True
    df.loc[df['RSI'] > SELL_THRESHOLD, 'signal'] = False

    # 보유여부
    df.loc[df['signal'].shift(1) == True, 'holding'] = True
    df.loc[df['signal'].shift(1) == False, 'holding'] = False
    df['holding'].ffill(inplace=True)
    df['holding'].fillna(False, inplace=True)

    # 마지막 보유여부가 판매면 팔아..
    # 마지막 보유여부가 구매면 사..
    # 근데 얼마를 사고팔지
    