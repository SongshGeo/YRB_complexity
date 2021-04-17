#!/usr/bin/env python 3.83
# -*-coding:utf-8 -*-
# @Author  : Shuang Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Research Gate: https://www.researchgate.net/profile/Song_Shuang9
from abc import ABC

from pandas.core.base import DataError
import pandas as pd
from pandas import DataFrame
from genepy_index import genepy_index
import numpy as np


class TradeTable(DataFrame, ABC):
    """
    为了方便分析地区/贸易表，创建一个继承自DataFrame的类
    """

    def data_validation(self):
        """
        检验数据的可行性：
        """
        pass

    def get_rca_matrix(self):
        """
        计算RCA矩阵，将贸易量与总贸易量相对比
        """
        up = self / self.sum()
        bottom = self.sum(axis=1) / self.sum().sum()
        rca_matrix = pd.DataFrame(index=self.index)
        for col in self:
            rca_matrix[col] = up[col] / bottom
        rca_matrix = rca_matrix.dropna(how='any', axis=0)
        return rca_matrix

    @property
    def get_bool_matrix(self):
        """
        利用RCA矩阵生成出口地区-出口商品的0-1矩阵
        """
        rca_matrix = self.get_rca_matrix()
        index, columns = rca_matrix.index, rca_matrix.columns
        rca_matrix[rca_matrix < 1] = 0
        rca_matrix[rca_matrix >= 1] = 1
        return pd.DataFrame(rca_matrix, index=index, columns=columns).astype(int)

    def calculate_genepy_index(self):
        """
        利用出口地区-出口商品的0-1矩阵，计算区域的经济复杂度指标
        """
        matrix = self.get_bool_matrix
        if matrix.shape[0] <= 1:
            raise DataError("No data in the bool matrix.")
        index = genepy_index(matrix)[1]
        return pd.Series(index.flatten(), index=matrix.index)
