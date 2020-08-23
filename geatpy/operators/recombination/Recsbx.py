# -*- coding: utf-8 -*-
from operators.recombination.Recombination import Recombination
from recsbx import recsbx

class Recsbx(Recombination):
    
    """
    Recsbx - class : 一个用于调用内核中的函数recsbx(模拟二进制交叉)的类，
                     该类的各成员属性与内核中的对应函数的同名参数含义一致，
                     可利用help(recsbx)查看各参数的详细含义及用法。
    """
    
    def __init__(self, XOVR = 0.7, Half = False, n = 20, Parallel = False):
        self.XOVR = XOVR # 发生交叉的概率
        self.Half = Half # 表示是否只保留一半交叉结果
        self.n = n # 分布指数，必须不小于0
        self.Parallel = Parallel # 表示是否采用并行计算，缺省时默认为False
    
    def do(self, OldChrom): # 执行内核函数
        return recsbx(OldChrom, self.XOVR, self.Half, self.n, self.Parallel)
    
    def getHelp(self): # 查看内核中的重组算子的API文档
        help(recsbx)
    