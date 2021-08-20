#!/usr/bin/env python 3.83
# -*-coding:utf-8 -*-
# Created date: 2021-05-15
# @Author  : Shuang Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Research Gate: https://www.researchgate.net/profile/Song_Shuang9

yellow_river_provinces = [
    'Henan',
    'Shandong',
    'Shanxi',
    'Shaanxi',
    # 'Sichuan',
    'Gansu',
    'Ningxia',
    'Neimeng',
    'Qinghai',
    # 'Hebei'
]

# 所有的相关作物
crop_list = [
    "wheat",
    "maize",
    "rice",
    "sorghum",
    "barley",
    "millet",
    "potato",
    "sweetpotato",
    "soybean",
    "groundnuts",
    "sunflower",
    "rapeseed",
    "sugarbeet",
    "sugarcane",
    "cotton",
    "spinach",
    "tomato",
    "cabbage",
    "apple",
    "grape",
    "tea",
    "tobacco"
]

ENG_NAME = {
    '淮河流域': 'Huai',
    '珠江流域': 'Zhu',
    '长江流域': 'Chang',
    '黄河流域': 'Yellow',
    '海河流域': 'Hai',
}


def export_virtue_water_matrix(data, y):
    """
    利用年份，提取省之间虚拟水贸易的量
    params: data, 数据表（total? green? blue?)
    params: y, 年份
    return: 省-作物，虚拟水出口量的数据表
    """
    case = data.groupby("Year").get_group(y)
    case.index = case["Province Name"]
    case = case.iloc[:, 3:]
    matrix = case[case < 0].abs().fillna(0.)
    return matrix
