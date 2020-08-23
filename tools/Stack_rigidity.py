"""根据装配后测试数据，反求偏心偏斜量"""
import numpy as np
from Prediction import Prediction as pre
import numpy as np


class Para():
    """
    获取所有参数
    """
    def __init__(self, runout, r):
        self.runout = runout
        self.r = r
        
    def vec(self, args):
        runout = args[0]
        r = args[1]
        theta = args[2]
        res = pre.pfit(pre.gcfl(r, pre.spin(runout, theta), 0))
        return res
    
    def cen(self, args):
        runout = args[0]
        r = args[1]
        theta = args[2]
        res = pre.circ(pre.gcra(r, pre.spin(runout, theta), 0))
        return res
    
    def getPara(self):
        runout = self.runout
        r = self.r
        para = [[]] * len(runout)
        for i in range(int(len(runout) / 4)):
            args_1 = list(zip([runout[i * 4]] * 36, [r[i * 4]] * 36, [i * 10 for i in range(36)]))
            args_2 = list(zip([runout[i * 4 + 1]] * 36, [r[i * 4 + 1]] * 36, [i * 10 for i in range(36)]))
            args_3 = list(zip([runout[i * 4 + 2]] * 36, [r[i * 4 + 2]] * 36, [i * 10 for i in range(36)]))
            args_4 = list(zip([runout[i * 4 + 3]] * 36, [r[i * 4 + 3]] * 36, [i * 10 for i in range(36)]))
            para[i * 4] = [i for i in map(self.vec, args_1)]
            para[i * 4 + 1] = [i for i in map(self.vec, args_2)]
            para[i * 4 + 2] = [i for i in map(self.cen, args_3)]
            para[i * 4 + 3] = [i for i in map(self.cen, args_4)]
        return para

    def spin_vec(self, args):
        vector = args[0]
        theta = args[1]
        a = vector[0]
        b = vector[1]
        c = vector[2]
        theta_2 = theta * np.pi / 180  # rad
        spin_vec = []
        spin_vec.append(a * np.cos(theta_2) - b * np.sin(theta_2))
        spin_vec.append(a * np.sin(theta_2) + b * np.cos(theta_2))
        spin_vec.append(c)
        spin_vec.append(vector[3])
        return spin_vec

    def spin_cen(self, args):
        center = args[0]
        theta = args[1]
        x = center[1]
        y = center[2]
        r = np.sqrt(x ** 2 + y ** 2)
        alpha = pre.get_phase(x, y)  # 角度值
        beta = -(theta - alpha)  # 角度值
        beta_2 = beta * np.pi / 180  # 转换为弧度
        spin_cen = []
        spin_cen.append(center[0])
        spin_cen.append(r * np.cos(beta_2))
        spin_cen.append(r * np.sin(beta_2))
        return spin_cen

    def getPara2(self):
        runout = self.runout
        r = self.r
        para = [[]] * len(r)
        for i in range(int(len(r) / 4)):
            vector_down = pre.pfit(pre.gcfl(r[i * 4], runout[i * 4], 0))
            vector_up = pre.pfit(pre.gcfl(r[i * 4 + 1], runout[i * 4 + 1], 0))
            args_1 = list(zip([vector_down] * 36, [-i * 10 for i in range(36)]))  # 需对相位取负结果才和之前一样，原因未知？？
            args_2 = list(zip([vector_up] * 36, [-i * 10 for i in range(36)]))
            para[i * 4] = [i for i in map(self.spin_vec, args_1)]
            para[i * 4 + 1] = [i for i in map(self.spin_vec, args_2)]

            center_down = pre.circ(pre.gcra(r[i * 4 + 2], runout[i * 4 + 2], 0))
            center_up = pre.circ(pre.gcra(r[i * 4 + 3], runout[i * 4 + 3], 0))
            args_3 = list(zip([center_down] * 36, [i * 10 for i in range(36)]))
            args_4 = list(zip([center_up] * 36, [i * 10 for i in range(36)]))
            para[i * 4 + 2] = [i for i in map(self.spin_cen, args_3)]
            para[i * 4 + 3] = [i for i in map(self.spin_cen, args_4)]
        return para


class Stack_rigidity():
    """
    刚性堆叠模型
    """
    def __init__(self, runout, r, H, para):
        self.runout = runout
        self.r = r
        self.H = H
        self.para = para
        
    def gcra(self, r, runout, h, theta):                #(generate coordinates--radial)生成止口的直角坐标；theta顺时针为正
        H = len(runout)
        Hr = np.round(theta / 360 * H)
        Hr = int(Hr)
        a = list(runout[Hr:H])
        b = list(runout[:Hr])
        a.extend(b)
        new_runout = np.array(a)
        t = np.linspace(np.pi / 1800, 2 * np.pi, 3600)
        x = (r + new_runout) * np.cos(t)
        y = (r + new_runout) * np.sin(t)
        z = np.array([h] * 3600)
        data = np.dstack((x, y, z))
        data = np.squeeze(data)
        return data
    
    def gcfl(self, r, runout, h, theta):                #(generate coordinates--flat)生成端面的直角坐标
        H = len(runout)
        Hr = np.round(theta / 360 * H)
        Hr = int(Hr)
        a = list(runout[Hr:H])
        b = list(runout[:Hr])
        a.extend(b)
        new_runout = np.array(a)
        t = np.linspace(0, 3599, 3600)
        x = r * np.cos(2 * np.pi * t / 3600)
        y = r * np.sin(2 * np.pi * t / 3600)
        z = h + new_runout
        data = np.dstack((x, y, z))
        data = np.squeeze(data)
        return data
    
    def get_phase(self, x, y):
        if x > 0:
            phase = np.arctan(y / x) * 180 / np.pi
        else:
            phase = np.arctan(y / x) * 180 / np.pi + 180
        return phase
    
    def bias_2(self, part1_theta, part2_theta):
        runout = self.runout
        r = self.r
        H = self.H
        #生成坐标
        part1_flat_coordinate_down = self.gcfl(r[0], runout[0], 0, part1_theta)
        part1_flat_coordinate_up = self.gcfl(r[1], runout[1], 0, part1_theta)
        part1_radial_coordinate_down = self.gcra(r[2], runout[2], 0, part1_theta)
        part1_radial_coordinate_up = self.gcra(r[3], runout[3], 0, part1_theta)
        #part1两端圆心及法向量
        part1_center_down = pre.circ(part1_radial_coordinate_down)
        part1_center_up = pre.circ(part1_radial_coordinate_up)
        part1_vector_down = pre.pfit(part1_flat_coordinate_down)
        part1_vector_up = pre.pfit(part1_flat_coordinate_up)
        #生成坐标
        part2_flat_coordinate_down = self.gcfl(r[4], runout[4], 0, part2_theta)
        part2_flat_coordinate_up = self.gcfl(r[5], runout[5], 0, part2_theta)
        part2_radial_coordinate_down = self.gcra(r[6], runout[6], 0, part2_theta)
        part2_radial_coordinate_up = self.gcra(r[7], runout[7], 0, part2_theta)
        #part2两端圆心及法向量
        part2_center_down = pre.circ(part2_radial_coordinate_down)
        part2_center_up = pre.circ(part2_radial_coordinate_up)
        part2_vector_down = pre.pfit(part2_flat_coordinate_down)
        part2_vector_up = pre.pfit(part2_flat_coordinate_up)
        #求出装配后偏心偏斜量
        part1_results = pre.eccentric(part1_center_down[1], part1_center_down[2], part1_center_up[1], part1_center_up[2], part1_vector_down[0], part1_vector_down[1], part1_vector_down[2], part1_vector_up[0], part1_vector_up[1], part1_vector_up[2], H[0])
        part2_results = pre.eccentric(part2_center_down[1], part2_center_down[2], part2_center_up[1], part2_center_up[2], part2_vector_down[0], part2_vector_down[1], part2_vector_down[2], part2_vector_up[0], part2_vector_up[1], part2_vector_up[2], H[1])
        part1_x_center = part1_results[0]
        part1_y_center = part1_results[1]
        part1_theta_y = part1_results[2]
        part1_theta_x = part1_results[3]
        part2_x_center = part2_results[0]
        part2_y_center = part2_results[1]
        part2_theta_y = part2_results[2]
        part2_theta_x = part2_results[3]
        p1 = np.array([[1, 0, part1_theta_y, part1_x_center], [0, 1, part1_theta_x, part1_y_center], [-part1_theta_y, -part1_theta_x, 1, H[0]], [0, 0, 0, 1]])
        p2 = np.array([[1, 0, part2_theta_y, part2_x_center], [0, 1, part2_theta_x, part2_y_center], [-part2_theta_y, -part2_theta_x, 1, H[1]], [0, 0, 0, 1]])
        m = np.matmul(p1, p2)
        #偏心量
        e = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
        #偏心相位
        phase = self.get_phase(m[0, 3], m[1, 3])
        return [e, phase]

    def bias_n_li_fast(self, theta):  #接收一个list类型的theta参数；返回【所有级】的结果
        # runout = self.runout
        # r = self.r
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(H)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        e, phase = [0] * (len(p)), [0] * (len(p))
        m = 1
        for i in range(len(p)):
            m = np.dot(m, p[i])
            #偏心量
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            #偏心相位
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
        return np.stack((e, phase), axis=1)

    def bias_n_li_fast_e_projection(self, theta):  #接收一个list类型的theta参数；分别返回【所有级】的e_projection【之和】
        H = self.H
        para = self.para
        p = [0] * (len(H))
        for i in range(len(H)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        # 保存各级零件偏心坐标
        center = np.zeros((len(p) + 1, 3))
        m = 1
        e, phase = [0] * (len(p)), [0] * (len(p))
        M = []
        M.append(np.zeros((4, 4)))
        for i in range(len(p)):
            m = np.dot(m, p[i])
            center[i + 1, :] = m[0:3, 3]
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
            M.append(m)
        rot_axis_vector = np.array([m[0, 3], m[1, 3], m[2, 3]])  # 实际回转轴线法向量
        a, b, c = rot_axis_vector
        e_projection = np.zeros((len(p), 1))
        for i in range(len(p)):
            le = np.sqrt((center[i + 1, 0] - center[0, 0]) ** 2 + (center[i + 1, 1] - center[0, 1]) ** 2 + (center[i + 1, 2] - center[0, 2]) **2)
            d = abs(a * center[i + 1, 0] + b * center[i + 1, 1] + c *  center[i + 1, 2]) / np.sqrt(a ** 2 + b ** 2 + c ** 2)  # 点到平面距离
            e_projection[i] = np.sqrt(abs(le ** 2 - d ** 2))
        return e_projection
    
    def get_rot_axis(self, theta):  #确定一个回转轴线
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(H)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        # 保存各级零件偏心坐标
        center = np.zeros((len(p) + 1, 3))
        m = 1
        M = []
        M.append(np.zeros((4, 4)))
        for i in range(len(p)):
            m = np.dot(m, p[i])
        rot_axis_vector = np.array([m[0, 3], m[1, 3], m[2, 3]])  # 实际回转轴线法向量
        return rot_axis_vector
    
    def plot_center(self, theta):  #接收一个list类型的theta参数；返回各级偏心坐标及相位
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(H)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        center = np.zeros((len(p) + 1, 3))
        m = 1
        for i in range(len(p)):
            m = np.dot(m, p[i])
            center[i + 1, :] = m[0:3, 3]
        return center

