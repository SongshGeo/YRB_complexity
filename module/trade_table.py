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
from module.genepy_index import genepy_index
import numpy as np
import networkx as nx
from tools.bipartite_network_explore import get_neighbors


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
        rca_matrix = rca_matrix.dropna(how='all', axis=0)
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
        return pd.DataFrame(rca_matrix, index=index, columns=columns).fillna(.0).astype(int)

    def calculate_genepy_index(self):
        """
        利用出口地区-出口商品的0-1矩阵，计算区域的经济复杂度指标
        """
        matrix = self.get_bool_matrix
        if matrix.shape[0] <= 1:
            raise DataError("No data in the bool matrix.")
        index = genepy_index(matrix)[1]
        return pd.Series(index.flatten(), index=matrix.index)

    def graph_copy_only_nodes(self):
        graph = nx.Graph()
        graph.add_nodes_from(self.columns, color='#006C43', bipartite='crops')
        graph.add_nodes_from(self.index, color='#C83C1C', bipartite='provinces')
        return graph

    def get_graph(self):
        """
        利用邻接矩阵，生成二分网络的图
        :return: networkx 图对象
        """
        graph = self.graph_copy_only_nodes()
        edges_list = []
        adj_matrix = self.get_bool_matrix.to_dict()
        for crop, dic in adj_matrix.items():
            for province in dic:
                if dic[province] > 0:
                    edges_list.append((crop, province))

        graph.add_edges_from(edges_list)
        return graph

    def get_knn_dict(self, axis=0, depth=1):
        """
        计算贸易二分网络的平均邻居度
        :param axis: 计算轴
        :param depth: 深度（第几层邻居）
        :return: 返回平均度
        """
        graph = self.get_graph()
        knn_dic = {}
        if axis == 0:
            use_list = self.index.tolist()
        elif axis == 1:
            use_list = self.columns.tolist()
        else:
            use_list = []
        for item in use_list:
            output = get_neighbors(graph, item, depth=depth)[depth]
            degree = graph.degree(item)
            if degree == 0:
                degree = 1
            knn = np.sum([graph.degree(n) for n in output]) / degree
            knn_dic[item] = knn
        return pd.Series(knn_dic, index=use_list)

    def mean_nbr_degree(self, **kwargs):
        """
        利用贸易矩阵制作的二元网络，计算平均最近邻居度（KNN）的全网平均值
        :param kwargs:
            :kwargs, axis: 计算轴
            :kwargs depth: 深度（第几层邻居）
        :return: 整个网络所有节点的KNN的全局平均值
        """
        return self.get_knn_dict(**kwargs).mean()

    def copy_absolute_random_graph(self):
        random_graph = self.graph_copy_only_nodes()
        refer_graph = self.get_graph()
        top = self.index.tolist()
        bottom = self.columns.tolist()

        k = len(refer_graph.edges)
        edge_count = 0
        while edge_count < k:
            # generate random edge,u,v
            u = np.random.choice(top)
            v = np.random.choice(bottom)
            if v in random_graph[u]:
                continue
            else:
                random_graph.add_edge(u, v)
                edge_count += 1
        return random_graph

    def copy_one_side_random_graph(self, top='index'):
        """
        制作一个与输入贸易网络类似的复杂网络：
            1- 两侧结点数量与边数量完全相同
            2- 某一侧节点度值的分布完全相同
            3- 另一侧结点连边目标随机
        :param top: 模仿哪一边的度分布? index, or column
        :return:随机网
        """
        if top == 'index':
            top = self.index.tolist()
            bottom = self.columns.tolist()
        elif top == 'column':
            top = self.columns.tolist()
            bottom = self.index.tolist()
        else:
            top, bottom = None, None

        random_graph = self.graph_copy_only_nodes()
        refer_graph = self.get_graph()

        for out_node in top:
            degree = refer_graph.degree(out_node)
            for in_node in np.random.choice(bottom, int(degree), replace=False):
                random_graph.add_edge(out_node, in_node)
        return random_graph
