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

    # 보유수익률

    df['holding_rev'] = df.loc[df['holding'] == True, 'daily_rev']
    df['holding_rev'].fillna(1, inplace=True)

    df['rsi_rev'] = df['holding_rev'].cumprod()
    df['just_holding_profit'] = df['close']/df.iloc[0, 0]

    # plot draw
    plt.rcParams['figure.dpi'] = 200
    df[['rsi_rev', 'just_holding_profit']].plot(figsize=(8, 4))
