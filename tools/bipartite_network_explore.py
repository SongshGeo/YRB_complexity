#!/usr/bin/env python
# -*-coding:utf-8 -*-
# Created date: 2021/5/20
# @Author  : Shuang Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Research Gate: https://www.researchgate.net/profile/Song_Shuang9
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np


def get_neighbors(g, node, depth=1):
    """
    获得一个网络，从某个节点出发，不同深度的关联结点
    :param g: 网络
    :param node: 从哪个点出发
    :param depth: 检索多少层
    :return: dict:
        key: 第xx层
        value: list, 该层与输入节点相关联
    """
    output = {}
    layers = dict(nx.bfs_successors(g, source=node, depth_limit=depth))
    nodes = [node]
    for i in range(1, depth+1):
        output[i] = []
        for x in nodes:
            output[i].extend(layers.get(x, []))
        nodes = output[i]
    return output


def get_mean_nearest_nbr_degree(g, depth=1):
    provinces = []
    for n in g:
        if nx.get_node_attributes(g, 'bipartite')[n] == 'provinces':
            provinces.append(n)
    degrees = []
    for item in provinces:
        output = get_neighbors(g, item, depth=depth)[depth]
        degree = g.degree(item)
        if degree == 0:
            degree = 1
        knn = np.sum([g.degree(n) for n in output]) / degree
        degrees.append(knn)
    return np.mean(degrees)


def plot_bipartite_graph(graph, top_attribute='provinces', ax=None):
    """
    绘制二分图
    :param top_attribute:
    :param graph:
    :param ax:
    :return:
    """
    if not ax:
        _, ax = plt.subplots()
    if not nx.is_bipartite(graph):
        return None
    top = []
    for n in graph:
        if nx.get_node_attributes(graph, 'bipartite')[n] == top_attribute:
            top.append(n)
    pos = nx.bipartite_layout(graph, top)
    color_map = [nx.get_node_attributes(graph, 'color')[n] for n in graph]
    nx.drawing.nx_pylab.draw_networkx(graph, pos=pos, node_color=color_map, node_size=100, font_size=10,
                                      edge_color='lightgray', ax=ax)
    return True
