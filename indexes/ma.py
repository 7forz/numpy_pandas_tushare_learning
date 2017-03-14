#!/usr/bin/python3
# -*- encoding: utf8 -*-

import numpy as np
from indexes.base import Index
import global_data


class MA(Index):
    """ 简单移动平均线 """

    def __init__(self, stock):
        super().__init__(stock)

    def get_ma(self, date, days=5):
        """ 获取给定日期的 days日均线 """
        data = global_data.get_data(self.stock)  # 数据库存在返回dataframe 否则返回None

        if data is not None:
            # 数据库存在分3种情况 有当天K线数据且已经算出来 有K线但NaN 和没有K线数据
            # 尝试从已有数据读取 读取成功马上返回
            try:
                result = data.loc[date, 'ma%s' % days]  # 若没有K线数据会抛出KeyError
                if str(result) != 'nan':  # 有K线但NaN result不是简单的np.nan
                    return result
                else:
                    raise RuntimeError
            except (KeyError, RuntimeError):
                # 没有数据 更新数据到最新
                data = global_data.update_data(self.stock)
                closes = data['close']
        else:
            # 无该股K线数据则从网上获取 再提取收盘价
            data = global_data.add_data(self.stock, start='2016-01-01')
            closes = data['close']

        # 计算MA
        if len(closes) > days:  # 避免只有50天数据却计算了MA90的问题 否则求卷积后提取时会有问题
            ma = self.ma(closes, days)
            new_data = global_data.add_column(self.stock, 'ma%s' % days, ma)  # 计算出来后填入总表
            return new_data.loc[date, 'ma%s' % days]  # 最终返回对应日期的MA值
        else:
            return np.nan