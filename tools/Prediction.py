# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 16:07:29 2020

@author: Lenovo
"""
from numpy import linalg as la
import numpy as np
import pandas as pd
# from numba import jit


class Prediction():
    """
    拟合法向量、圆心
    """
    
    def idata(ad, usecols):
        """
        导入第n列数据
        """
        data = np.array(pd.read_csv(ad, usecols=usecols))
        data = np.squeeze(data)
        return data
    
    def gcfl(r, runout, H):
        """
        (generate coordinates--flat)生成端面的直角坐标
        """
        theta = np.linspace((2 * np.pi) / len(runout), 2 * np.pi, len(runout))
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = H + runout
        data = np.stack((x, y, z), axis=1)
        return data
    
    # @jit
    def pfit(data):
        """
        (plane fit)拟合平面法向量
        """
        U,sigma,VT = la.svd(data)
        if VT[2, 2] < 0:
            VT[2, :] = -VT[2, :]
        a = VT[2, 0]
        b = VT[2, 1]
        c = VT[2, 2]
        d = -a * data[0, 0] - b * data[0, 1] - c * data[0, 2]
        result = np.array([a, b, c, d])
        return result
    
    def gcra(r, runout, H):
        """
        (generate coordinates--radial)生成止口的直角坐标
        """
        theta = np.linspace((2 * np.pi) / len(runout), 2 * np.pi, len(runout))
        x = (r + runout) * np.cos(theta)
        y = (r + runout) * np.sin(theta)
        z = np.array([H] * len(runout))
        data = np.dstack((x, y, z))
        data = np.squeeze(data)
        return data
    
    # @jit
    def circ(data):
        """
        返回最小二乘法拟合圆心
        """
        x = data[:, 0]
        y = data[:, 1]
        x1, x2, x3, y1, y2, y3, x1y1, x1y2, x2y1 = 0, 0, 0, 0, 0, 0, 0, 0, 0
        N = len(data[:, 0])
        for i in range(N):
            x1 = x1 + x[i]
            x2 = x2 + x[i] * x[i]
            x3 = x3 + x[i] * x[i] * x[i]
            y1 = y1 + y[i]
            y2 = y2 + y[i] * y[i]
            y3 = y3 + y[i] * y[i] * y[i]
            x1y1 = x1y1 + x[i] * y[i]
            x1y2 = x1y2 + x[i] * y[i] * y[i]
            x2y1 = x2y1 + x[i] * x[i] * y[i]
        C = N * x2 - x1 * x1
        D = N * x1y1 - x1 * y1
        E = N * x3 + N * x1y2 - (x2 + y2) * x1
        G = N * y2 - y1 * y1
        H = N * x2y1 + N * y3 - (x2 + y2) * y1
        a = (H * D - E * G) / (C * G - D * D)
        b = (H * C - E * D) / (D * D - G * C)
        c = -(a * x1 + b * y1 + x2 + y2) / N
        A = a/(-2)
        B = b/(-2)
        R = np.sqrt(a * a + b * b - 4 * c) / 2
        result = [R, A, B]
        return result
    
    def spin(runout, theta):
        """
        旋转形貌数据
        """
        H = len(runout)
        Hr = np.round(theta / 360 * H)
        Hr = int(Hr)
        a = list(runout[Hr:H])
        b = list(runout[:Hr])
        a.extend(b)
        new_runout = np.array(a)
        return new_runout
    
    def eccentric(A1, B1, A2, B2, a1, b1, c1, a2, b2, c2, L):
        """
        单体等效模型矩阵
        """
        a = a2 / c2 - a1 / c1
        b = b2 / c2 - b1 / c1
        A = A2 - A1 + L * np.sin(-a1 / c1)
        B = B2 - B1 + L * np.sin(-b1 / c1)
        result = [A, B, a, b]
        return result

    def get_phase(x, y):
        """
        由坐标获取角度值
        """
        if x > 0:
            phase = np.arctan(y / x) * 180 / np.pi
        else:
            phase = np.arctan(y / x) * 180 / np.pi + 180
        return phase

    # @jit
    def translation(data, x, y, z):
        """
        对每一组坐标（3×1）进行平移变换
        """
        TM = np.array([[1,0,0,x], [0,1,0,y], [0,0,1,z], [0,0,0,1]])
        S = []
        for i in range(len(data[:, 0])):
            data_1 = np.array([data[i, 0], data[i, 1], data[i, 2], 1]).reshape(-1,1)
            S1 = np.dot(TM, data_1)
            S.append(S1[0])
            S.append(S1[1])
            S.append(S1[2])
        S = np.array(S).reshape(-1,3)
        return S
    
    # @jit
    def rotation(data, x, y, z):
        """
        对每一组坐标（3×1）进行旋转变换
        """
        Rotx = np.array([[1,0,0,0], [0,np.cos(x),-np.sin(x),0], [0,np.sin(x),np.cos(x),0], [0,0,0,1]])
        Roty = np.array([[np.cos(y),0,np.sin(y),0], [0,1,0,0], [-np.sin(y),0,np.cos(y),0], [0,0,0,1]])
        Rotz = np.array([[np.cos(z),-np.sin(z),0,0], [np.sin(z),np.cos(z),0,0], [0,0,1,0], [0,0,0,1]])
        TR = np.dot(Rotz, np.dot(Rotx, Roty))
        S = []
        for i in range(len(data[:, 0])):
            data_1 = np.array([data[i, 0], data[i, 1], data[i, 2], 1]).reshape(-1,1)
            S1 = np.dot(TR, data_1)
            S.append(S1[0])
            S.append(S1[1])
            S.append(S1[2])
        S = np.array(S).reshape(-1,3)
        return S