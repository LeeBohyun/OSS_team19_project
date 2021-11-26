import pandas_datareader.data as web
import datetime
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import pickle
from tqdm import tqdm

with open('codes.pickle','rb') as f:
    codes = pickle.load(f)
class stock:
    def __init__(self,code,gs):
        self.code = code
        self.gs = gs
    def get_data(self,days):
        self.open_list = self.gs['Open'][-days-1:-1]
        self.volume_list = self.gs['Volume'][-days-1:-1]
        self.last_open = self.gs['Open'][-1]
        self.last_volume = self.gs['Volume'][-1]
        if self.open_list[-2] < self.open_list[-1]:
            self.increase = True
        else:
            self.increase = False

stock_list=[]
for c in tqdm(codes):
    found=False
    try:
        gs = web.DataReader(c+'.KS', 'yahoo')
        found=True
    except:
        found=False
    if not found:
        try:
            gs = web.DataReader(c+'.KQ', 'yahoo')
            found=True
        except:
            found=False
    if found:
        # print(c, 'success')
        stock_list.append(stock(c,gs))
    else:
        # print(c, 'fail')
        pass
with open('stock_list.pickle','wb') as f:
    pickle.dump(stock_list,f)