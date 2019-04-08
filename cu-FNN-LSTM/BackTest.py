# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:16:19 2019

@author: 54326
"""
from math import sqrt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_nav(record, retn, trans_cost=0, slippage=0):
    '''
    计算净值
    '''
    test_retn = pd.concat([record, retn], axis=1, join='inner')
    if slippage:
        trans_cost += slippage # 将滑点算入交易成本
    test_retn['l_s'] = np.where(test_retn[record.name] != 0, # 交易收益等于交易记录标签与实际收益率的乘积
             test_retn[record.name] * abs(test_retn[retn.name]) - trans_cost, 0) 
    test_retn['nav'] = test_retn['l_s'].cumsum() + 1 # 累计收益率
    return test_retn#['nav']

def maxdd(nav):
    '''
    根据净值序列计算最大回撤序列
    '''
    DD = []
    for i in range(1, len(nav)):
        max_i = max(nav[:i])
        DD.append(min((nav[i] - max_i) / max_i,  0))
    return pd.Series(DD, index=nav.index[1:], name='max drawdown')

def evaluate(nav):
    '''
    计算最大回撤，年化收益率，calmar比率等评价指标
    '''
    mdd = maxdd(nav.nav) # 最大回撤
    nav['duration'] = 0
    duration_idx = nav.columns.tolist().index('duration')
    for i in range(1, len(nav)):
        if mdd[i-1] == 0:
            nav.iloc[i, duration_idx] = 0
        else:
            nav.iloc[i, duration_idx] = nav.iloc[i-1, duration_idx] + 1
    ann = (nav.nav[-1] / nav.nav[0]) ** (242 / len(nav)) - 1 # 年化收益率
    calmar = abs(ann / mdd.min()) # calmar比率
    nav['e'] = (nav.l_s - (0.03 / 242))
    sharpe = nav.e.mean() / nav.e.std() * sqrt(242)
    win = len(nav[nav.e > 0]) / len(nav[nav.l_s != 0])
    return nav['duration'].max(), mdd, ann, calmar, sharpe, win

def nav_plot(nav, fig_size=(12, 8)):
    '''
    绘制回测曲线图
    '''
    mddd, mdd, ann, calmar, sharpe, win = evaluate(nav)
    ddd_idx = nav['duration'].idxmax()
    ddd_begin = nav.loc[:ddd_idx, 'nav'].idxmax()
    ddd_center = nav.index[(len(nav.loc[:ddd_begin, :]) + len(nav.loc[:ddd_idx, :])) // 2]
    dd_idx = mdd.idxmin()
    dd_begin = nav.loc[:dd_idx, 'nav'].idxmax()
    fig, ax = plt.subplots(figsize=fig_size)
    idx = nav.index
    ax.plot(idx, nav.nav)
    ax.set_xlim(idx[0], idx[-1])
    ax.set_ylabel('Net Aseet Value', fontsize=10)
    offset = (nav.nav.max() - nav.nav.min()) / 20
    ax.annotate("", xy=(ddd_idx, nav.nav[ddd_begin]), xycoords='data',
                 xytext=(ddd_begin, nav.nav[ddd_begin]), textcoords='data',
                 arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
    ax.text(ddd_center, nav.nav[ddd_begin]+offset*1.2, 'max drawdown duration', 
            {'color': 'k', 'fontsize': 12, 'ha': 'center', 'va': 'top',})
    ax.annotate("", xy=(dd_idx, nav.nav[dd_begin]), xycoords='data', 
                xytext=(dd_idx, nav.nav[dd_idx]), textcoords='data',
                arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
    ax.text(dd_idx, nav.nav[dd_idx]-offset, 'max drawdown',
            {'color': 'k', 'fontsize': 12, 'ha': 'center', 'va': 'bottom',})
    ax2 = ax.twinx()
    ax2.set_ylim(-1, 0)
    ax2.plot(mdd, color='c')
    ax2.fill_between(idx[1:], mdd, color='c')
    ax2.set_ylabel('Max Drawdown', fontsize=10)
    ax2.text(ax2.get_xbound()[0]+5, -0.97, 
             'Max Drawdwon Duration: %d, Max Drawdown: %.2f%%, Annual: %.2f%%, Calmar: %.2f, sharpe: %.2f, win: %.2f' % 
             (mddd, mdd.min() *100, ann*100, calmar, sharpe, win))