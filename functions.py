import pandas_datareader.data as web
import datetime
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import pickle
import sys
from sklearn.linear_model import LogisticRegression



class x_y:
    def __init__(self,days):
        with open('stock_list_small.pickle','rb') as f:
            stock_list = pickle.load(f)
        pass_fail = []
        for stock in stock_list:
            try:
                stock.get_data(days)
                pass_fail.append(True)
            except:
                pass_fail.append(False)
        x_with_zeros= np.zeros(shape=(np.sum(pass_fail),days*2),dtype=np.int)
        y=[]
        idx=0
        for idx, s in enumerate(stock_list):
            if pass_fail[idx]:
                try:
                    x_with_zeros[idx,:] = list(list(s.open_list[:-1].values)+list(s.volume_list[:-1].values))
                    y.append(s.increase)
                except:
                    pass
                idx+=1
        x= np.zeros(shape=(len(y),days*2),dtype=np.int)
        zero_num=0
        for idx, x_ in enumerate(x_with_zeros):
            if np.sum(x_)==0:
                pass
            else:
                x[zero_num,:] = x_
                zero_num+=1
        self.x = x
        self.y = y
        self.days=days

class stock_bot:
    def __init__(self,x,y,days):
        self.org_x = x.copy()
        self.org_y = y.copy()
        self.days = days
        self.x = x.copy()
        self.y = y.copy()
    def set_org(self):
        self.x = self.org_x
        self.y = self.org_y
    def set_x_price_par(self,p):
        self.x[:,:self.days] = self.org_x[:,:self.days]*p
    def set_x_volume_par(self,p):
        self.x[:,self.days:] = self.org_x[:,self.days:]*p
    def ret_clf(self):
        return LogisticRegression(random_state=0).fit(self.x,self.y)

class stock_bot_final:
    def __init__(self,days,p1,p2):
        self.xy = x_y(days)
        self.sb = stock_bot(self.xy.x,self.xy.y,self.xy.days)
        self.sb.set_x_price_par(p1)
        self.sb.set_x_volume_par(p2)
    def ret_clf(self):
        self.clf= LogisticRegression(random_state=0).fit(self.sb.x,self.sb.y)
        return self.clf
    def validate(self):
        right=0
        wrong = 0
        for idx, x_ in enumerate(self.xy.x):
            if(self.clf.predict(x_.reshape(1,-1))[0]==self.xy.y[idx]):
                right+=1
            else:
                wrong+=1
        print(right,wrong)
        with open('model_accuracy.txt','w',encoding='utf-8') as f:
            f.write(str(right)+':'+str(wrong))

class stock:
    def __init__(self,code,gs):
        self.code = code
        self.gs = gs
    def get_data(self,days):
        self.open_list = self.gs['Open'][-days-1:]
        self.volume_list = self.gs['Volume'][-days-1:]
        if self.open_list[-2] < self.open_list[-1]:
            self.increase = True
        else:
            self.increase = False

class sample_obj:
    def __init__(self,stock_list,num):
        self.sample_stocks = stock_list[:num]
        self.stock_list = stock_list
    def get_data(self,days):
        for s in self.sample_stocks:
            s.get_data(days)
    def get_xy(self,days):
        stock_list = self.sample_stocks
        pass_fail = []
        for stock in stock_list:
            try:
                stock.get_data(days)
                pass_fail.append(True)
            except:
                pass_fail.append(False)
        x_with_zeros= np.zeros(shape=(np.sum(pass_fail),days*2),dtype=np.int)
        y=[]
        idx=0
        for idx, s in enumerate(stock_list):
            if pass_fail[idx]:
                try:
                    x_with_zeros[idx,:] = list(list(s.open_list[:-1].values)+list(s.volume_list[:-1].values))
                    y.append(s.increase)
                except:
                    pass
                idx+=1
        x= np.zeros(shape=(len(y),days*2),dtype=np.int)
        zero_num=0
        for idx, x_ in enumerate(x_with_zeros):
            if np.sum(x_)==0:
                pass
            else:
                x[zero_num,:] = x_
                zero_num+=1
        self.x = x
        self.y = y
        self.days=days
    def get_xy_par(self,days,par1,par2):
        self.get_xy(days)
        self.x[:,:days] = self.x[:,:days]*par1
        self.x[:,days:] = self.x[:,days:]*par2
    def predict(self,clf):
        pass

def sorting(stock_list, num,days,p1,p2):
    so = sample_obj(stock_list,num)
    so.get_xy_par(days,p1,p2)
    sbf = stock_bot_final(days,p1,p2)
    clf = sbf.ret_clf()
    sbf.validate()
    ret = np.asarray(clf.predict_proba(so.x.reshape(num,-1))[:,1])
    #print(ret)
    sorting_ret = np.argsort(ret*-1)
    return sorting_ret

def sorting2(stock_list, num, days, p1, p2):
    so = sample_obj(stock_list,num)
    so.get_xy_par(days,p1,p2)
    sbf = stock_bot_final(days,p1,p2)
    clf = sbf.ret_clf()
    sbf.validate()
    ret = np.asarray(clf.predict_proba(so.x.reshape(num,-1))[:,1])
    #print(ret)
    sorting_ret = np.argsort(ret*-1)
    sorting_ret2 = np.sort(ret*-1)
    return sorting_ret,sorting_ret2*-1

def sorting3(stock_list,num,days,p1,p2):
    so = sample_obj(stock_list,num)
    so.get_xy_par(days,p1,p2)
    sbf = stock_bot_final(days,p1,p2)
    clf = sbf.ret_clf()
    sbf.validate()
    prob = np.asarray(clf.predict_proba(so.x.reshape(num,-1))[:,1])
    cost = np.zeros(num,dtype=np.int)
    for idx in range(num):
        cost[idx] = stock_list[idx].open_list[-1]
    return prob, cost

samples= [
['000040', 'KR모터스'],
['000050', '경방'],
['000060', '메리츠화재'],
['000070', '삼양홀딩스'],
['000075', '삼양홀딩스우'],
['000080', '하이트진로'],
['000087', '하이트진로2우B'],
['000100', '유한양행'],
['000105', '유한양행우'],
['000120', 'CJ대한통운'],
['000140', '하이트진로홀딩스'],
['000145', '하이트진로홀딩스우'],
['000150', '두산'],
['000155', '두산우'],
['000157', '두산2우B'],
]


# main codes

with open('stock_list.pickle', 'rb') as f:
    stock_list = pickle.load(f)
a, b = sorting3(stock_list, 15, int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
with open('stock_info.txt','w',encoding='utf-8') as f:
    for idx in range(15):
        print(samples[idx][1],'Prob : ',a[idx], ' Price : ',b[idx])
        f.write(samples[idx][1]+':'+str(b[idx])+':'+'%.2f\n'%(a[idx]*100))


def main():
    print('main')


if __name__ == '___main__':
    
    main()

