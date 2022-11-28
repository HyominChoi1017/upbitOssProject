import pyupbit
 

# for i in pyupbit.get_tickers():
#     try:
#         current_price = pyupbit.get_current_price(i)
#         print('{}: {}'.format(i, current_price))
#     except:
#         pass


# print(pyupbit.get_current_price(pyupbit.get_tickers))

df = pyupbit.get_ohlcv("KRW-BTC")
print(df)