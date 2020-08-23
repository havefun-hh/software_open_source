# -*- coding: utf-8 -*-
from operators.recombination.Recombination import Recombination
from xovpmx import xovpmx

class Xovpmx(Recombination):
    
    """
    Xovpmx - class : 一个用于调用内核中的函数xovpmx(部分匹配交叉)的类，
                     该类的各成员属性与内核中的对应函数的同名参数含义一致，
                     可利用help(xovpmx)查看各参数的详细含义及用法。
                     
    """
    
    def __init__(self, XOVR = 0.7, Half = False, Method = 1, Parallel = False):
        self.XOVR = XOVR # 发生交叉的概率
        self.Half = Half # 表示是否只保留一半交叉结果
        self.Method = Method # 表示部分匹配交叉采用什么方法进行交叉。
        self.Parallel = Parallel # 表示是否采用并行计算，缺省时默认为False
    
    def do(self, OldChrom): # 执行内核函数
        return xovpmx(OldChrom, self.XOVR, self.Half, self.Method, self.Parallel)
    
    def getHelp(self): # 查看内核中的重组算子的API文档
        help(xovpmx)
    