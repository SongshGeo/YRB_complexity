#!/usr/bin/env python 3.83
# -*-coding:utf-8 -*-
# Created date: 2021-08-20
# @Author  : Shuang Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Research Gate: https://www.researchgate.net/profile/Song_Shuang9

from matplotlib import pyplot as plt

def plot_gam_and_interval(x, y, main_color='#29303C', err_color="gray", width=0.95, ax=None, err_space=True, alpha=0.1, scatter_alpha=0.8, y_label="Y"):
    if not ax:
        fig, ax = plt.subplots()
        
    from pygam import LinearGAM
    X = x.reshape(-1, 1)
    
    gam = LinearGAM(n_splines=25).gridsearch(X, y)
    XX = gam.generate_X_grid(term=0, n=500)
    
    ax.plot(XX, gam.predict(XX), color=main_color, label="{} GAM Fitted".format(y_label))  # 拟合曲线
    ax.scatter(X, y, facecolor=main_color, alpha=scatter_alpha, label="")  # 散点
    
    if err_space:
        err = gam.prediction_intervals(XX, width=width)
        ax.plot(XX, gam.prediction_intervals(XX, width=width), color=err_color, ls='--')  # 置信区间
        ax.fill_between(XX.reshape(-1,), err[:,0], err[:,1], color=err_color, alpha=alpha, label='{} Confidence interval'.format(y_label))
