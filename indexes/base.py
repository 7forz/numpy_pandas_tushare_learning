#!/usr/bin/python3
# -*- encoding: utf8 -*-

import numpy as np


class Index():
    
    def __init__(self, stock):
        self.stock = stock

    def ma(self, array, days):
        """ 计算简单移动平均线 传入一个array和days 返回一个array """
        _weights = np.ones(days) / days  # 权重相等
        ma = np.convolve(_weights, array)[days-1:1-days]  # 求出(array-days+1)天的MA(days) 最早的(days-1)天缺数据
        ma = np.concatenate( (np.array([np.nan] * (days-1)), ma) )  # 缺数据所以填入(days-1)个nan 确保长度相等日期对齐
        return ma

    def ema(self, array, days):
        """ 计算指数移动平均线 传入一个array和days 返回一个array """
        _result = [array[0]]  # result初始值定为array的初值
        for i in range(1, len(array)):  # 后面的进行递归计算
            # EMA(N) = 前一日EMA(N) X (N-1)/(N+1) + 今日收盘价 X 2/(N+1)
            # e.g.
            # EMA(9) = 前一日EMA(9) X 8/10 + 今日收盘价 X 2/10
            _result.append(_result[i-1] * (days-1) / (days+1) + array[i] * 2 / (days+1))
        assert len(array) == len(_result)
        return np.array(_result)  # 返回一个np.array而不是list对象