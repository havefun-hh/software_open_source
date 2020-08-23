# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 18:22:41 2020

@author: admin
"""
import numpy as np
import geatpy as ea   # import geatpy


class MyProblem_aim3(ea.Problem): # 继承Problem父类
    """
    自定义目标函数类
    """
    def __init__(self, aim, n, Dim, phase):
        self.aim = aim
        self.n = n
        self.phase = phase
        name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
        M = 1 # 初始化M（目标维数）
        maxormins = [1] # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        #Dim = 2 # 初始化Dim（决策变量维数）——只考虑两级装配，只有一个自变量（端跳差分值）
        Dim = Dim
        varTypes = [1] * Dim # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim # 决策变量下界
        ub = [35] * Dim # 决策变量上界
        lbin = [1] * Dim # 决策变量下边界
        ubin = [1] * Dim # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
    
    def aimFunc(self, pop): # 目标函数
        aim = self.aim
        n = self.n
        phase = self.phase
        Vars = pop.Phen # 得到决策变量矩阵
        f = np.zeros((len(Vars[:, 0]), 1))
        for i in range(len(Vars[:, 0])):
            if phase == None:
                x = [0] + [j * 10 for j in Vars[i, :]]  # 注意Vars的切片要×10
                f[i] = sum(aim.bias_n_li_fast_e_projection(x))
            else:
                x = phase + [j * 10 for j in Vars[i, :]]
                f[i] = sum(aim.bias_n_li_fast_e_projection(x))
        pop.ObjV = f # 计算目标函数值，赋值给pop种群对象的ObjV属性



