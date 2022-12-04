from dataPrepare import prepareData
from greedy_fear_index import fear_last_6month
from prophet import Prophet
import matplotlib.pyplot as plt

ppd = prepareData()
fng = fear_last_6month()

# 나중에는 그냥 decision에서 데이터 한번 불러온 후에 param으로 전달해야지.

def fngModel():
    '''
    공포탐욕지수가 0에 가깝다. -> Extreme Fear (하락장)
    공포탐욕지수가 100에 가깝다. -> Extreme Greedy (상승장)
    공포탐욕지수가 50에 가깝다. -> 중립.

    < index의 threshold는 나중에 선정... >
    (index >= 70) -> 구매에 1표
    (index <= 30) -> 판매에 1표
    ㄴ 탐욕장(상승장 분위기)이면 사야지
    ㄴ 공포장(하락장 분위기)이면 팔아야지
    '''
    global fng
    m = Prophet()
    df = fng.reset_index()
    df['ds'] = df['index']
    df['y'] = df['fngIndex']
    data = df[['ds', 'y']]

    m.fit(data)
    future = m.make_future_dataframe(periods=7, freq='D')
    forecast = m.predict(future)
    # print('----- 나온다~ ------')
    print(forecast[-7:]['yhat'])
    # m.plot(forecast)

    idx =  (forecast.iloc[-7:])['yhat'].mean()
    
    return idx

# print(fngModel())    

def closePriceModel():
    global ppd 
    m = Prophet()
    df = ppd.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds', 'y']]
    
    m.fit(data)
    # 향후 12시간의 가격을 예측
    future = m.make_future_dataframe(periods=24, freq='H')
    forecast = m.predict(future)
    f1 = m.plot(forecast) 
    f2 = m.plot_components(forecast) 
    # plt.show()
    trd = forecast[-24:]['trend']
    print(forecast[-24:])
    trd = (trd.iloc[-1] - trd.iloc[0])/24
    # if trd > 0:
    #     print('다음 24시간동안 상승트렌드이다~')
    # elif trd == 0:
    #     print('그대로다')
    # else:
    #     print('하락한다.')

    return trd


closePriceModel()