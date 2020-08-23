# -*- coding: utf-8 -*-
import os
import numpy as np

class Problem:
    
    """
Problem : Class - 问题类

描述:
    问题类是用来存储与待求解问题相关信息的一个类。

属性:
    name      : str   - 问题名称（可以自由设置名称）。
    
    M         : int   - 目标维数，即有多少个优化目标。
    
    maxormins : array - 目标函数最小最大化标记的行向量，1表示最小化，-1表示最大化，例如：
                        array([1,1,-1,-1])，表示前2个目标是最小化，后2个目标是最大化。
    
    Dim       : int   - 决策变量维数，即有多少个决策变量。
    
    varTypes  : array - 连续或离散标记，是Numpy array类型的行向量，
                        0表示对应的决策变量是连续的；1表示对应的变量是离散的。
    
    ranges    : array - 决策变量范围矩阵，第一行对应决策变量的下界，第二行对应决策变量的上界。
    
    borders   : array - 决策变量范围的边界矩阵，第一行对应决策变量的下边界，第二行对应决策变量的上边界，
                        0表示范围中不含边界，1表示范围包含边界。

函数:
    aimFunc(pop) : 目标函数，需要在继承类即自定义的问题类中实现，或是传入已实现的函数。
                   其中pop为Population类的对象，代表一个种群，
                   pop对象的Phen属性（即种群染色体的表现型）等价于种群所有个体的决策变量组成的矩阵，
                   该函数根据该Phen计算得到种群所有个体的目标函数值组成的矩阵，并将其赋值给pop对象的ObjV属性。
                   若有约束条件，则在计算违反约束程度矩阵CV后赋值给pop对象的CV属性（详见Geatpy数据结构）。
                   该函数不返回任何的返回值，求得的目标函数值保存在种群对象的ObjV属性中。
                   例如：population为一个种群对象，则调用aimFunc(population)即可完成目标函数值的计算，
                   此时可通过population.ObjV得到求得的目标函数值，population.CV得到违反约束程度矩阵。
    
    calReferObjV()   : 计算目标函数参考值，需要在继承类中实现，或是传入已实现的函数。
    
    getReferObjV()   : 获取目标函数参考值。

"""

    def __init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin, aimFunc = None, calReferObjV = None):
        self.name = name
        self.M = M
        self.maxormins = np.array(maxormins)
        self.Dim = Dim
        self.varTypes = np.array(varTypes)
        self.ranges = np.array([lb, ub]) # 初始化ranges（决策变量范围矩阵）
        self.borders = np.array([lbin, ubin]) # 初始化borders（决策变量范围边界矩阵）
        self.aimFunc = aimFunc if aimFunc is not None else self.aimFunc # 初始化目标函数接口
        self.calReferObjV = calReferObjV if calReferObjV is not None else self.calReferObjV # 初始化理论最优值计算函数接口
    
    def aimFunc(self, pop):
        raise RuntimeError('error in Problem: aimFunc has not been initialized. (未在问题子类中设置目标函数！)')
    
    def calReferObjV(self):
        return None
    
    def getReferObjV(self, reCalculate = False):
        
        """
        描述: 该函数用于读取/计算问题的目标函数参考值，这个参考值可以是理论上的全局最优解的目标函数值，也可以是人为设定的非最优的目标函数参考值。
        reCalculate是一个bool变量，用于判断是否需要调用calReferObjV()来重新计算目标函数参考值。
        默认情况下reCalculate是False，此时将先尝试读取理论全局最优解的数据，
        若读取不到，则尝试调用calReferObjV()来计算理论全局最优解。
        在计算理论全局最优解后，
        将结果按照“问题名称_目标维数_决策变量个数.csv”的文件命名把数据保存到referenceObjV文件夹内。
        
        """
        
        if os.path.exists('referenceObjV') == False:
            os.makedirs('referenceObjV')
        if reCalculate == False:
            # 尝试读取数据
            if os.path.exists('referenceObjV/' + self.name + '_M' + str(self.M) + '_D' + str(self.Dim) + '.csv'):
                return np.loadtxt('referenceObjV/' + self.name + '_M' + str(self.M) + '_D' + str(self.Dim) + '.csv', delimiter=',')
        # 若找不到数据，则调用calReferObjV()计算目标函数参考值
        referenceObjV = self.calReferObjV()
        if referenceObjV is not None:
            # 保存数据
            np.savetxt('referenceObjV/' + self.name + '_M' + str(self.M) + '_D' + str(self.Dim) + '.csv', referenceObjV, delimiter=',')
        else:
            print('未找到目标函数参考值数据！')
        return referenceObjV
