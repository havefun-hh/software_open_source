# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test0701.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

import os
import sys
root_path = os.getcwd()  # 获取当前路径
sys.path.append(root_path + "\\geatpy\\core")
sys.path.append(root_path + "\\geatpy")
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QMainWindow, QDialog, QFileDialog, QLabel, QLineEdit, QTextEdit, QMessageBox, \
    QSplashScreen, QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QAction
import pyqtgraph as pg
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
import numpy as np
import geatpy as ea
import time
from pandas import read_csv
from tools.MyProblem_2 import MyProblem_aim3  # 导入自定义问题接口
from Stack_rigidity import Stack_rigidity, Para
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import resource


class Ui_MainWindow(QMainWindow):
    is_saved = True
    is_saved_first = True
    path = ''
    def __init__(self):
        """
        初始化 UI 界面
        """
        super(Ui_MainWindow, self).__init__()
        self.setWindowTitle("软件")
        self.resize(1200, 720)
        # 定义函数，使启动时窗口居中
        self.center()
        self.demo = QTabWidget()
        self.setCentralWidget(self.demo)

        # 添加菜单栏
        # self.file_menu = QtWidgets.QMenuBar(self)
        self.file_menu = self.menuBar().addMenu('File')
        self.help_menu = self.menuBar().addMenu('Help')
        self.menu_init()
        self.action_init()

        # 添加状态栏
        self.status_bar = QtWidgets.QStatusBar(self)
        self.status_bar.setObjectName("statusbar")
        self.setStatusBar(self.status_bar)
        self.status_bar_init()

        # 添加tab窗口
        self.tab1 = QWidget()  # 1
        self.tab4 = QTextEdit()
        self.cursor = self.tab4.textCursor()  # 属于 tab4 的游标

        self.tab1_init()  # 2

        self.demo.addTab(self.tab1, '预测及优化')  # 3
        self.demo.addTab(self.tab4, '结果及导出')

        sys.stdout = Stream(newText=self.onUpdateText)
        self.consoleBox = QTextEdit(self, readOnly=True)
        self.demo.addTab(self.consoleBox, QIcon(':images/info.ico'), '操作记录')  # 5

        self.demo.currentChanged.connect(lambda: print(time.strftime("%Y-%m-%d %H:%M:%S $"), f'tab{self.demo.currentIndex() + 1}'))

    def menu_init(self):
        """
        初始化菜单栏
        """
        self.new_action = QAction('New', self)
        self.open_action = QAction('Open', self)
        self.save_action = QAction('Save', self)
        self.save_as_action = QAction('Save As', self)
        self.about_action = QAction('About', self)

        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        # self.menufile.addSeparator()  # 添加分隔条
        self.help_menu.addAction(self.about_action)

    def status_bar_init(self):
        """
        初始化状态栏
        """
        self.status_bar.showMessage('Ready!')
        self.status_label = QLabel()
        self.statusBar().addPermanentWidget(self.status_label)

    def action_init(self):
        """
        初始化动作
        """
        self.new_action.setIcon(QIcon('images/new.ico'))  # 1
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.setToolTip('Create a new file')
        self.new_action.setStatusTip('Create a new file')
        self.new_action.triggered.connect(self.new_func)

        self.open_action.setIcon(QIcon('images/open.ico'))  # 2
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setToolTip('Open an existing file')
        self.open_action.setStatusTip('Open an existing file')
        self.open_action.triggered.connect(self.open_file_func)

        self.save_action.setIcon(QIcon('images/save.ico'))  # 3
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setToolTip('Save the file')
        self.save_action.setStatusTip('Save the file')
        # self.save_action.triggered.connect(lambda: self.save_func(self.tab4.toHtml()))  # 保存为 html 文件
        self.save_action.triggered.connect(lambda: self.save_func(self.tab4.toPlainText()))

        self.save_as_action.setIcon(QIcon('images/save_as.ico'))
        self.save_as_action.setShortcut('Ctrl+A')
        self.save_as_action.setToolTip('Save the file to a specified location')
        self.save_as_action.setStatusTip('Save the file to a specified location')
        self.save_as_action.triggered.connect(lambda: self.save_as_func(self.tab4.toPlainText()))

        self.about_action.setIcon(QIcon('images/about.ico'))  # 11
        self.about_action.setShortcut('Ctrl+Q')
        self.about_action.setToolTip('What is Qt?')
        self.about_action.setStatusTip('What is Qt?')
        self.about_action.triggered.connect(self.about_func)

    def new_func(self):
        """
        槽函数：新建文件
        """
        if not self.is_saved and self.tab4.toPlainText():
            choice = QMessageBox.question(self, '', 'Do you want to save the text?',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func(self.tab4.toPlainText())
                self.tab4.clear()
                self.is_saved_first = True
            elif choice == QMessageBox.No:
                self.tab4.clear()
            else:
                pass
        else:
            self.tab4.clear()
            self.is_saved = False
            self.is_saved_first = True

    def open_file_func(self):
        """
        槽函数：打开文件
        """
        if not self.is_saved:
            choice = QMessageBox.question(self, '', 'Do you want to save the text?',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func(self.tab4.toPlainText())
                file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Files (*.html *.txt *.log *.py *.md)')
                if file:
                    with open(file, 'r') as f:
                        self.tab4.clear()
                        self.tab4.setText(f.read())
                        self.is_saved = True
            elif choice == QMessageBox.No:
                file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Files (*.html *.txt *.log *.py *.md)')
                if file:
                    with open(file, 'r') as f:
                        self.tab4.clear()
                        self.tab4.setText(f.read())
                        self.is_saved = True
            else:
                pass
        else:
            file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Files (*.html *.txt *.log *.py *.md)')
            if file:
                with open(file, 'r') as f:
                    self.tab4.clear()
                    self.tab4.setText(f.read())
                    self.is_saved = True

    def save_func(self, text):
        """
        槽函数：保存文件
        """
        if self.is_saved_first:
            self.save_as_func(text)
        else:
            with open(self.path, 'w') as f:
                f.write(text)
            self.is_saved = True

    def save_as_func(self, text):
        """
        槽函数：另存为文件
        """
        self.path, _ = QFileDialog.getSaveFileName(self, 'Save File', './', 'Files (*.html *.txt *.log *.py *.md)')
        if self.path:
            with open(self.path, 'w') as f:
                f.write(text)
            self.is_saved = True
            self.is_saved_first = False

    def about_func(self):
        """
        槽函数：About 信息
        """
        QMessageBox.aboutQt(self, 'About Qt')

    def center(self):
        """
        启动时居中
        """
        # 1
        desktop = QApplication.desktop()
        d_width = desktop.width()
        d_height = desktop.height()

        # 2
        pos_x = d_width / 2 - self.frameGeometry().width() / 2
        pos_y = d_height / 2 - self.frameGeometry().height() / 2

        # 3
        self.move(int(pos_x), int(pos_y))

    def idata(self, ad, usecols):
        """
        (import data)导入第n列数据
        """
        data = np.array(read_csv(ad, usecols=usecols))
        data = np.squeeze(data)
        return data

    def tab1_init(self):
        """
        第一个标签页窗口功能：装配精度预测
        """
        self.tab1.setStyleSheet("background-image: url(:images/background1.jpg);")
        self.frame = QtWidgets.QMainWindow()

        self.frame1 = QtWidgets.QFrame(self.tab1)
        self.frame1.setStyleSheet("background-image: url(:images/frame1.jpg);")
        self.frame1.setGeometry(QtCore.QRect(30, 25, 440, 600))
        self.frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame1.setObjectName("frame")
        # self.frame.
        self.frame1_groupbox_1 = QGroupBox('输入跳动数据', self.tab1)
        self.frame1_groupbox_2 = QGroupBox('输入参数', self.tab1)
        self.frame1_groupbox_3 = QGroupBox('预测结果', self.tab1)
        self.frame1_groupbox_1.setStyleSheet('background-image: url(:images/groupbox1.jpg);')
        self.frame1_groupbox_2.setStyleSheet('background-image: url(:images/groupbox2.jpg);')
        self.frame1_groupbox_3.setStyleSheet('background-image: url(:images/groupbox3.jpg);')
        self.frame1_init()

        self.frame2 = QtWidgets.QFrame(self.tab1)
        self.frame2.setGeometry(QtCore.QRect(500, 25, 670, 600))
        self.frame2.setStyleSheet("background-image: url(:images/frame2.jpg);")
        self.frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame2.setObjectName("frame")
        self.frame2_init()

        self.tab1_status_bar = QtWidgets.QStatusBar(self.frame)
        self.frame.setStatusBar(self.tab1_status_bar)
        self.tab1_status_bar.showMessage('123')

    def frame1_init(self):
        """
        第一个标签页窗口的子窗口1（导入跳动数据、输入参数、输出预测值）
        """
        # 第一个groupbox组合框
        self.frame1_input_button = QtWidgets.QPushButton('导入', self.frame1)
        self.frame1_input_button.setStatusTip('导入跳动数据，格式为：')
        self.frame1_test_button = QtWidgets.QPushButton('test', self.frame1)
        self.frame1_test_button.setStatusTip('测试按钮')
        self.frame1_test_button.setIcon(QIcon(':images/button.png'))
        self.frame1_test_button.clicked.connect(self.para_init2)
        frame1_layout1 = QHBoxLayout()
        frame1_layout1.addWidget(self.frame1_input_button)
        frame1_layout1.addStretch(1)
        frame1_layout1.addWidget(self.frame1_test_button)
        self.frame1_groupbox_1.setLayout(frame1_layout1)

        # 第二个groupbox组合框
        self.frame1_label_1 = QLabel('前轴', self.frame1)
        self.frame1_label_2 = QLabel('一级盘', self.frame1)
        self.frame1_label_3 = QLabel('二级盘', self.frame1)
        self.frame1_label_4 = QLabel('三级盘', self.frame1)
        self.frame1_label_5 = QLabel('涡轮盘', self.frame1)
        self.frame1_label_6 = QLabel('后轴', self.frame1)

        self.frame1_label_h = QLabel('h/mm', self.frame1)
        self.frame1_line_1_h = QLineEdit(self.frame1)
        self.frame1_line_2_h = QLineEdit(self.frame1)
        self.frame1_line_3_h = QLineEdit(self.frame1)
        self.frame1_line_4_h = QLineEdit(self.frame1)
        self.frame1_line_5_h = QLineEdit(self.frame1)
        self.frame1_line_6_h = QLineEdit(self.frame1)

        self.frame1_label_r1 = QLabel('r1/mm', self.frame1)
        self.frame1_line_1_r1 = QLineEdit(self.frame1)
        self.frame1_line_2_r1 = QLineEdit(self.frame1)
        self.frame1_line_3_r1 = QLineEdit(self.frame1)
        self.frame1_line_4_r1 = QLineEdit(self.frame1)
        self.frame1_line_5_r1 = QLineEdit(self.frame1)
        self.frame1_line_6_r1 = QLineEdit(self.frame1)

        self.frame1_label_r2 = QLabel('r2/mm', self.frame1)
        self.frame1_line_1_r2 = QLineEdit(self.frame1)
        self.frame1_line_2_r2 = QLineEdit(self.frame1)
        self.frame1_line_3_r2 = QLineEdit(self.frame1)
        self.frame1_line_4_r2 = QLineEdit(self.frame1)
        self.frame1_line_5_r2 = QLineEdit(self.frame1)
        self.frame1_line_6_r2 = QLineEdit(self.frame1)

        self.frame1_label_r3 = QLabel('r3/mm', self.frame1)
        self.frame1_line_1_r3 = QLineEdit(self.frame1)
        self.frame1_line_2_r3 = QLineEdit(self.frame1)
        self.frame1_line_3_r3 = QLineEdit(self.frame1)
        self.frame1_line_4_r3 = QLineEdit(self.frame1)
        self.frame1_line_5_r3 = QLineEdit(self.frame1)
        self.frame1_line_6_r3 = QLineEdit(self.frame1)

        self.frame1_label_r4 = QLabel('r4/mm', self.frame1)
        self.frame1_line_1_r4 = QLineEdit(self.frame1)
        self.frame1_line_2_r4 = QLineEdit(self.frame1)
        self.frame1_line_3_r4 = QLineEdit(self.frame1)
        self.frame1_line_4_r4 = QLineEdit(self.frame1)
        self.frame1_line_5_r4 = QLineEdit(self.frame1)
        self.frame1_line_6_r4 = QLineEdit(self.frame1)

        self.frame1_label_phase = QLabel('相位/°', self.frame1)
        self.frame1_line_1_phase = QLineEdit(self.frame1)
        self.frame1_line_2_phase = QLineEdit(self.frame1)
        self.frame1_line_3_phase = QLineEdit(self.frame1)
        self.frame1_line_4_phase = QLineEdit(self.frame1)
        self.frame1_line_5_phase = QLineEdit(self.frame1)
        self.frame1_line_6_phase = QLineEdit(self.frame1)

        self.frame1_button1 = QtWidgets.QPushButton('初始化', self.frame1)
        self.frame1_button1.setStatusTip('填充默认的 h 和 r')
        self.frame1_button1.setIcon(QIcon(':images/Bell.ico'))
        self.frame1_button1.clicked.connect(self.para_init)  # 注意此处的槽函数无括号
        self.frame1_button2 = QtWidgets.QPushButton('清空', self.frame1)
        self.frame1_button2.setStatusTip('清空以上所有参数')
        self.frame1_button2.setIcon(QIcon(':images/clear.png'))
        self.frame1_button2.clicked.connect(self.para_clear)
        self.frame1_button3 = QtWidgets.QPushButton('导入新的参数表', self.frame1)
        self.frame1_button3.setStatusTip('导入参数表，格式为：')

        frame1_layout2 = QVBoxLayout()
        g_layout = QGridLayout()
        g_layout.addWidget(self.frame1_label_1, 1, 0, 1, 1)
        g_layout.addWidget(self.frame1_label_2, 2, 0, 1, 1)
        g_layout.addWidget(self.frame1_label_3, 3, 0, 1, 1)
        g_layout.addWidget(self.frame1_label_4, 4, 0, 1, 1)
        g_layout.addWidget(self.frame1_label_5, 5, 0, 1, 1)
        g_layout.addWidget(self.frame1_label_6, 6, 0, 1, 1)
        g_layout.addWidget(self.frame1_label_h, 0, 1, 1, 1)
        g_layout.addWidget(self.frame1_line_1_h, 1, 1, 1, 1)
        g_layout.addWidget(self.frame1_line_2_h, 2, 1, 1, 1)
        g_layout.addWidget(self.frame1_line_3_h, 3, 1, 1, 1)
        g_layout.addWidget(self.frame1_line_4_h, 4, 1, 1, 1)
        g_layout.addWidget(self.frame1_line_5_h, 5, 1, 1, 1)
        g_layout.addWidget(self.frame1_line_6_h, 6, 1, 1, 1)
        g_layout.addWidget(self.frame1_label_r1, 0, 2, 1, 1)
        g_layout.addWidget(self.frame1_line_1_r1, 1, 2, 1, 1)
        g_layout.addWidget(self.frame1_line_2_r1, 2, 2, 1, 1)
        g_layout.addWidget(self.frame1_line_3_r1, 3, 2, 1, 1)
        g_layout.addWidget(self.frame1_line_4_r1, 4, 2, 1, 1)
        g_layout.addWidget(self.frame1_line_5_r1, 5, 2, 1, 1)
        g_layout.addWidget(self.frame1_line_6_r1, 6, 2, 1, 1)
        g_layout.addWidget(self.frame1_label_r2, 0, 3, 1, 1)
        g_layout.addWidget(self.frame1_line_1_r2, 1, 3, 1, 1)
        g_layout.addWidget(self.frame1_line_2_r2, 2, 3, 1, 1)
        g_layout.addWidget(self.frame1_line_3_r2, 3, 3, 1, 1)
        g_layout.addWidget(self.frame1_line_4_r2, 4, 3, 1, 1)
        g_layout.addWidget(self.frame1_line_5_r2, 5, 3, 1, 1)
        g_layout.addWidget(self.frame1_line_6_r2, 6, 3, 1, 1)
        g_layout.addWidget(self.frame1_label_r3, 0, 4, 1, 1)
        g_layout.addWidget(self.frame1_line_1_r3, 1, 4, 1, 1)
        g_layout.addWidget(self.frame1_line_2_r3, 2, 4, 1, 1)
        g_layout.addWidget(self.frame1_line_3_r3, 3, 4, 1, 1)
        g_layout.addWidget(self.frame1_line_4_r3, 4, 4, 1, 1)
        g_layout.addWidget(self.frame1_line_5_r3, 5, 4, 1, 1)
        g_layout.addWidget(self.frame1_line_6_r3, 6, 4, 1, 1)
        g_layout.addWidget(self.frame1_label_r4, 0, 5, 1, 1)
        g_layout.addWidget(self.frame1_line_1_r4, 1, 5, 1, 1)
        g_layout.addWidget(self.frame1_line_2_r4, 2, 5, 1, 1)
        g_layout.addWidget(self.frame1_line_3_r4, 3, 5, 1, 1)
        g_layout.addWidget(self.frame1_line_4_r4, 4, 5, 1, 1)
        g_layout.addWidget(self.frame1_line_5_r4, 5, 5, 1, 1)
        g_layout.addWidget(self.frame1_line_6_r4, 6, 5, 1, 1)
        g_layout.addWidget(self.frame1_label_phase, 0, 6, 1, 1)
        g_layout.addWidget(self.frame1_line_1_phase, 1, 6, 1, 1)
        g_layout.addWidget(self.frame1_line_2_phase, 2, 6, 1, 1)
        g_layout.addWidget(self.frame1_line_3_phase, 3, 6, 1, 1)
        g_layout.addWidget(self.frame1_line_4_phase, 4, 6, 1, 1)
        g_layout.addWidget(self.frame1_line_5_phase, 5, 6, 1, 1)
        g_layout.addWidget(self.frame1_line_6_phase, 6, 6, 1, 1)
        k_layout = QHBoxLayout()
        k_layout.addWidget(self.frame1_button1)
        k_layout.addWidget(self.frame1_button2)
        k_layout.addWidget(self.frame1_button3)
        frame1_layout2.addLayout(g_layout)
        frame1_layout2.addLayout(k_layout)
        self.frame1_groupbox_2.setLayout(frame1_layout2)

        # 第三个groupbox组合框
        self.frame1_predict_button = QtWidgets.QPushButton('预测', self.frame1)      # 连接4个槽函数
        self.frame1_predict_button.setStatusTip('预测装配精度')
        self.frame1_predict_button.setIcon(QIcon(':images/predict.png'))
        self.frame1_predict_button.clicked.connect(self.frame1_get_para_r_h)        # 接收参数 r, h
        self.frame1_predict_button.clicked.connect(self.frame1_get_para_phase)      # 接受参数 phase
        self.frame1_predict_button.clicked.connect(self.show_predict_messagebox)    # 提示消息框
        self.frame1_predict_button.clicked.connect(self.predict_execute)        # 预测主函数
        self.frame1_optimize_button = QtWidgets.QPushButton('优化', self.frame1)     # 连接3个槽函数
        self.frame1_optimize_button.setStatusTip('遗传算法寻找最优安装相位')
        self.frame1_optimize_button.setIcon(QIcon(':images/optimize.ico'))
        self.frame1_optimize_button.clicked.connect(self.frame1_get_para_r_h)       # 接收参数 r, h
        self.frame1_optimize_button.clicked.connect(self.show_optimize_messagebox)  # 提示消息框
        self.frame1_optimize_button.clicked.connect(self.optimize_execute)      # 优化主函数
        self.frame1_predict_clear_button = QtWidgets.QPushButton('清空', self.frame1)
        self.frame1_predict_clear_button.clicked.connect(self.frame1_clear_predict)
        self.frame1_predict_clear_button.setIcon(QIcon(':images/clear.png'))
        self.frame1_optimize_clear_button = QtWidgets.QPushButton('清空', self.frame1)
        self.frame1_optimize_clear_button.clicked.connect(self.frame1_clear_optimize_value_2)
        self.frame1_optimize_clear_button.setIcon(QIcon(':images/clear.png'))
        self.frame1_output_pvalue_label = QLabel('投影偏心值/mm', self.frame1)
        self.frame1_output_value_label = QLabel('偏心值/mm', self.frame1)
        self.frame1_output_phase_label = QLabel('偏心相位/°', self.frame1)
        self.frame1_predict_value_line = QLineEdit(self.frame1)
        self.frame1_predict_phase_line = QLineEdit(self.frame1)
        self.frame1_optimize_pvalue_line = QLineEdit(self.frame1)
        self.frame1_optimize_value_line = QLineEdit(self.frame1)
        self.frame1_optimize_phase_line = QLineEdit(self.frame1)
        h_layout = QGridLayout()
        h_layout.addWidget(self.frame1_output_pvalue_label, 0, 1)
        h_layout.addWidget(self.frame1_output_value_label, 0, 2)
        h_layout.addWidget(self.frame1_output_phase_label, 0, 3)
        h_layout.addWidget(self.frame1_predict_button, 1, 0)
        h_layout.addWidget(self.frame1_predict_value_line, 1, 2)
        h_layout.addWidget(self.frame1_predict_phase_line, 1, 3)
        h_layout.addWidget(self.frame1_predict_clear_button, 1, 4)
        h_layout.addWidget(self.frame1_optimize_button, 2, 0)
        h_layout.addWidget(self.frame1_optimize_pvalue_line, 2, 1)
        h_layout.addWidget(self.frame1_optimize_value_line, 2, 2)
        h_layout.addWidget(self.frame1_optimize_phase_line, 2, 3)
        h_layout.addWidget(self.frame1_optimize_clear_button, 2, 4)
        self.frame1_groupbox_3.setLayout(h_layout)

        # 垂直合并
        v1_layout = QVBoxLayout()
        v1_layout.addWidget(self.frame1_groupbox_1)
        v1_layout.addStretch(1)
        v1_layout.addWidget(self.frame1_groupbox_2)
        v1_layout.addStretch(1)
        v1_layout.addWidget(self.frame1_groupbox_3)

        self.frame1.setLayout(v1_layout)

        # 默认导入一组跳动数据
        ad_part1 = 'data/MNJ-HPC-002ZP1-20190709.csv'  # new_part1
        ad_part2 = 'data/MNJ-HPT-001ZP1-20190708.csv'  # part2
        ad_part3 = 'data/MNJ-HPC-001ZP2-20190708.csv'  # part1
        # new_part1--part2--part1--part2--new_part1--part1
        self.runout_default = np.stack((-self.idata(ad_part1, [3]), self.idata(ad_part1, [1]), self.idata(ad_part1, [4]),
                                        -self.idata(ad_part1, [2]), -self.idata(ad_part2, [4]), self.idata(ad_part2, [2]),
                                        self.idata(ad_part2, [3]), self.idata(ad_part2, [1]), -self.idata(ad_part3, [3]),
                                        self.idata(ad_part3, [1]), self.idata(ad_part3, [4]), self.idata(ad_part3, [2]),
                                        -self.idata(ad_part2, [4]), self.idata(ad_part2, [2]), self.idata(ad_part2, [3]),
                                        self.idata(ad_part2, [1]), -self.idata(ad_part1, [3]), self.idata(ad_part1, [1]),
                                        self.idata(ad_part1, [4]), -self.idata(ad_part1, [2]), -self.idata(ad_part3, [3]),
                                        self.idata(ad_part3, [1]), self.idata(ad_part3, [4]), self.idata(ad_part3, [2])), axis=0)
        self.frame1_line_r = [self.frame1_line_1_r1, self.frame1_line_1_r2, self.frame1_line_1_r3,
                              self.frame1_line_1_r4,
                              self.frame1_line_2_r1, self.frame1_line_2_r2, self.frame1_line_2_r3,
                              self.frame1_line_2_r4,
                              self.frame1_line_3_r1, self.frame1_line_3_r2, self.frame1_line_3_r3,
                              self.frame1_line_3_r4,
                              self.frame1_line_4_r1, self.frame1_line_4_r2, self.frame1_line_4_r3,
                              self.frame1_line_4_r4,
                              self.frame1_line_5_r1, self.frame1_line_5_r2, self.frame1_line_5_r3,
                              self.frame1_line_5_r4,
                              self.frame1_line_6_r1, self.frame1_line_6_r2, self.frame1_line_6_r3,
                              self.frame1_line_6_r4]
        self.frame1_line_h = [self.frame1_line_1_h, self.frame1_line_2_h, self.frame1_line_3_h, self.frame1_line_4_h,
                              self.frame1_line_5_h, self.frame1_line_6_h]
        self.frame1_line_phase = [self.frame1_line_1_phase, self.frame1_line_2_phase, self.frame1_line_3_phase,
                                  self.frame1_line_4_phase, self.frame1_line_5_phase, self.frame1_line_6_phase]
        self.r_default = None
        self.h_default = None
        self.phase = None
        self.step = 0
        self.predict_button_flag = 1
        self.optimize_button_flag = 1

    def frame2_init(self):
        """
        第一个标签页窗口的子窗口2（可视化展示）
        """
        pg.setConfigOption('background', 'w')  # 注：设置需在建立窗口之前，否则窗口为默认设置
        pg.setConfigOption('foreground', 'k')

        self.frame2_tab = QTabWidget()

        # 第二种方式添加图（多张）
        self.frame2_win1 = pg.GraphicsLayoutWidget(show=False, title="examples")
        self.frame2_p1 = self.frame2_win1.addPlot(row=0, col=0, title='遗传算法收敛图')   # 添加空图例
        self.frame2_p1.setLabel('left', "值/mm")
        self.frame2_p1.setLabel('bottom', "进化代数")

        self.frame2_button = QtWidgets.QPushButton('清除图像', self.frame2)
        self.frame2_button.setStyleSheet("background-image: url(:images/clear_image_button.jpg);")
        self.frame2_button.clicked.connect(self.frame1_clear_optimize_fig_2)
        self.frame2_button.setIcon(QIcon(':images/clear.png'))

        self.frame2_p2 = Figure_Canvas()
        # 对于三维图，我们需要重新定义一个三维的轴，因此需要先删除原来的轴
        self.frame2_p2.ax.remove()
        self.frame2_ax = self.frame2_p2.fig.gca(projection='3d', title=u'等效模型', xlabel='x', ylabel='y')

        self.frame2_tab.addTab(self.frame2_p2, '装配示意图')
        self.frame2_tab.addTab(self.frame2_win1, '遗传算法收敛图')

        frame2_layout = QVBoxLayout()
        frame2_layout.addWidget(self.frame2_tab)
        frame2_layout.addWidget(self.frame2_button)

        self.frame2.setLayout(frame2_layout)

        self.first_close = 0   # 设置标记第一次启动时，如果没有点击优化按钮，清空按钮不会清除图像

    def para_init(self):
        """
        参数 r, h 初始化
        r1 : 底端端跳半径
        r2 : 顶端端跳半径
        r3 : 底端径跳半径
        r4 : 顶端径跳半径
        """
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '初始化')
        # self.status.showMessage('初始化默认参数', 0)  #状态栏本身显示的信息 第二个参数是信息停留的时间，单位是毫秒，默认是0（0表示在下一个操作来临前一直显示）
        self.r_default = [84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 206.5 / 2, 84 / 2, 200 / 2, 80 / 2,
                          84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 206.5 / 2, 84 / 2, 200 / 2, 80 / 2,
                          84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 84 / 2, 206.5 / 2, 80 / 2, 200 / 2]
        self.h_default = [192, 120, 192, 120, 192, 192]
        for line_r, value_r in zip(self.frame1_line_r, self.r_default):
            line_r.setText(str(value_r))
        for line_h, value_h in zip(self.frame1_line_h, self.h_default):
            line_h.setText(str(value_h))

    def para_init2(self):   # 只初始化 2 级零件
        """
        参数 r, h 初始化
        r1 : 底端端跳半径
        r2 : 顶端端跳半径
        r3 : 底端径跳半径
        r4 : 顶端径跳半径
        """
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), 'test')
        # self.status.showMessage('初始化默认参数', 0)  #状态栏本身显示的信息 第二个参数是信息停留的时间，单位是毫秒，默认是0（0表示在下一个操作来临前一直显示）
        self.r_default = [84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 206.5 / 2, 84 / 2, 200 / 2, 80 / 2,
                          84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 206.5 / 2, 84 / 2, 200 / 2, 80 / 2,
                          84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 84 / 2, 206.5 / 2, 80 / 2, 200 / 2]
        self.h_default = [192, 120, 192, 120, 192, 192]
        for line_r, value_r in zip(self.frame1_line_r[4:12], self.r_default[4:12]):
            line_r.setText(str(value_r))
        for line_h, value_h in zip(self.frame1_line_h[1:3], self.h_default[1:3]):
            line_h.setText(str(value_h))

    def para_clear(self):
        """
        清空参数 r, h, phase
        """
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '清空所有参数')
        for line in (self.frame1_line_r + self.frame1_line_h + self.frame1_line_phase):
            line.clear()
        # 同时将self默认的r和h清空
        self.r_default = None
        self.h_default = None

    def frame1_get_para_r_h(self):
        """
        获取输入的参数 r, h
        """
        self.r_default = []
        for line_r in self.frame1_line_r:
            if line_r.text():
                self.r_default.append(float(line_r.text()))  # 通过text()方法获取输入框文本
        self.h_default = []
        for line_h in self.frame1_line_h:
            if line_h.text():
                self.h_default.append(float(line_h.text()))

    def frame1_get_para_phase(self):
        """
        获取输入的参数 phase
        """
        self.phase = []
        for line_phase in self.frame1_line_phase:
            if line_phase.text():
                self.phase.append(eval(line_phase.text()))

    def predict_execute(self):
        """
        检查是否满足函数运行条件，并弹出提示框
        """
        if self.h_default and self.r_default and self.phase and self.predict_button_flag:
            if len(self.h_default) == (len(self.r_default) / 4) == len(self.phase) and self.check_phase_isdigit():
                print(time.strftime("%Y-%m-%d %H:%M:%S $"), '开始预测')
                self.predict_button_flag = 0  # 设置标记为 0，单次运行完毕后重新置为1，防止连续多次点击
                # 添加提示窗口 Dialog
                self.dialog_predict = QDialog()
                self.dialog_predict.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.dialog_predict.resize(225, 70)
                self.dialog_predict.setStyleSheet("background-color: rgb(0, 170, 255);")
                self.dialog_predict.setWindowTitle('请稍等')
                self.dialog_label = QLabel('正在预测中，请稍等...0s', self.dialog_predict)  # 1
                self.dialog_layout = QHBoxLayout()
                self.dialog_layout.addWidget(self.dialog_label)
                self.dialog_predict.setLayout(self.dialog_layout)
                self.dialog_layout.deleteLater()
                self.dialog_predict.show()
                # 注：此处一定要先创建一个 QWidget，然后将 QTimer 写入其中，否则再次计算使，时间成倍增长？？
                self.dialog_widget = QWidget()
                self.timer = QTimer(self.dialog_widget)
                self.timer.timeout.connect(lambda: self.update_time('预测'))
                if not self.timer.isActive():
                    self.timer.start(100)
                # 创建线程
                self.predict = PRThread(self.runout_default, self.r_default, self.h_default, self.phase)
                # 启动线程
                self.predict.start()
                # 线程自定义信号连接的槽函数
                self.predict.trigger.connect(self.predict_display)
            elif len(self.h_default) == (len(self.r_default) / 4) == len(self.phase) and not self.check_phase_isdigit():
                QMessageBox.information(self, '提示', '相位为 0～359 之间的整数', QMessageBox.Ok)
            else:
                QMessageBox.information(self, '提示', '请检查输入参数', QMessageBox.Ok)

    def check_phase_isdigit(self):
        """
        判断输入的相位是否为整数，且范围在 0~359 之间
        """
        check = []
        for line_phase in self.frame1_line_phase:
            if line_phase.text():
                check.append(str(eval(line_phase.text())).isdigit() and eval(line_phase.text()) >= 0 and eval(line_phase.text()) <= 359)
        return all(check)

    def predict_display(self, pr_list):
        """
        预测结果显示
        """
        value = pr_list[0]  # 0——偏心值
        phase = pr_list[1]  # 1——偏心相位
        phase_list = pr_list[2]  # 2——
        aim = pr_list[3]  # 3——
        self.predict_button_flag = pr_list[4]  # 4——标记
        start = pr_list[5][0]  # 5——耗时
        end = pr_list[5][1]  # 5——耗时

        self.frame1_predict_value_line.setText(str(value))
        self.frame1_predict_phase_line.setText(str(phase))
        self.draw_figure(aim.plot_center(self.phase))
        self.status_label.setText(str(f'预测耗时：{self.step / 10}s'))
        self.timer.stop()
        self.step = 0
        self.dialog_predict.close()
        self.draw_figure(aim.plot_center(phase_list))

        self.cursor.movePosition(QtGui.QTextCursor.End)
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '预测偏心值为：%s mm\n' % value)
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '预测偏心相位为：%s°\n' % phase)
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + f'时间已过 {int((end - start) // 60)} 分 {(end - start) % 60:.8f} 秒\n')
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '==============================================================================\n')
        self.tab4.setTextCursor(self.cursor)
        self.tab4.ensureCursorVisible()

    def optimize_main_dialog(self):
        """
        检查是否满足函数运行条件，并弹出提示框
        """
        if self.h_default and self.r_default and self.optimize_button_flag:
            self.optimize_button_flag = 0
            if len(self.h_default) == (len(self.r_default) / 4) and len(self.h_default) > 1:
                # 添加提示窗口 Dialog yze.setWindowTitle('请稍等')
                self.dialog_widget = QWidget()
                self.timer = QTimer(self.dialog_widget)
                self.timer.timeout.connect(self.update_time)
                self.optimize = GAThread(self.runout_default, self.r_default, self.h_default, self.timer)
                self.status_label.setText(str(f'耗时：{self.step}s'))
                self.step = 0
            else:
                QMessageBox.information(self, '提示', '请检查输入参数', QMessageBox.Ok)

    def optimize_execute(self):
        """
        检查是否满足优化函数运行条件，并新建一个线程用来优化，防止界面出现假死现象
        """
        if self.h_default and self.r_default and self.optimize_button_flag:
            self.optimize_button_flag = 0
            if len(self.h_default) == (len(self.r_default) / 4) and len(self.h_default) > 1:
                print(time.strftime("%Y-%m-%d %H:%M:%S $"), '开始优化')
                # 添加提示窗口 Dialog （不影响 optimize_main 函数的运行）
                self.dialog_optimize = QDialog()
                self.dialog_optimize.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 设置窗口置顶
                self.dialog_optimize.resize(225, 70)
                self.dialog_optimize.setWindowTitle('请稍等')
                self.dialog_label = QLabel('正在优化中，请稍等...0s', self.dialog_optimize)  # 1
                self.dialog_layout = QHBoxLayout()
                self.dialog_layout.addWidget(self.dialog_label)
                self.dialog_optimize.setLayout(self.dialog_layout)
                self.dialog_layout.deleteLater()
                self.dialog_optimize.show()
                self.dialog_widget = QWidget()
                self.timer = QTimer(self.dialog_widget)
                self.timer.timeout.connect(lambda: self.update_time('优化'))
                if not self.timer.isActive():
                    self.timer.start(100)
                # 创建线程
                self.optimize = GAThread(self.runout_default, self.r_default, self.h_default)
                # 启动线程
                self.optimize.start()
                # 线程自定义信号连接的槽函数
                self.optimize.trigger.connect(self.optimize_display)
            else:
                QMessageBox.information(self, '提示', '请检查输入参数', QMessageBox.Ok)

    def optimize_display(self, op_list):
        """
        线程自定义信号连接的槽函数
        用来显示输出结果及可视化绘制
        """
        # 由于自定义信号时自动传递一个字符串参数，所以在这个槽函数中要接收一个参数
        pvalue = op_list[0]  # 0——投影偏心值
        value = op_list[1]  # 1——偏心值
        phase = op_list[2]  # 2——偏心相位
        find_index = op_list[3]  # 3——最优值索引位置
        n = op_list[4]  # 4——n
        res = op_list[5]  # 5——各级零件偏心结果res
        var_trace_shape_1 = op_list[6]  # 6——var_trace.shape[1]

        phase_list = op_list[7]  # 6——优化得到的安装相位
        self.gen = op_list[8]  # 7——种群进化代数
        self.obj_trace = op_list[9]  # 8——目标函数值
        aim = op_list[10]  # 9——目标对象
        obj_trace_shape_0 = op_list[11]  # 11——有效进化代数：obj_trace.shape[0]
        best_gen = op_list[12]  # 12——最优进化代数
        myAlgorithm_evalsNum = op_list[13]  # 13——评价次数
        start = op_list[14][0]  # 14——耗时
        end = op_list[14][1]  # 14——耗时
        self.optimize_button_flag = op_list[15]  # 15——传回 flag 标记，防止多次点击重复运行

        self.frame1_optimize_pvalue_line.setText(str(pvalue))  # round设置输出小数位数
        self.frame1_optimize_value_line.setText(str(value))
        self.frame1_optimize_phase_line.setText(str(phase))
        for i in range(6):
            if self.frame1_line_h[i].text():
                oo = i  # 找到输入的第一级零件的位置
                break
        for i, line in zip([i for i in range(len(phase_list))],
                           self.frame1_line_phase[oo:oo + len(phase_list)]):  # 有几级零件，则显示几个结果
            line.setText((str(int(phase_list[i]))))
        self.status_label.setText(str(f'优化耗时：{self.step / 10}s'))
        self.timer.stop()
        self.step = 0
        self.dialog_optimize.close()
        self.plot_objective_value_2()
        self.draw_figure(aim.plot_center(phase_list))
        self.cursor.movePosition(QtGui.QTextCursor.End)
        # 法一：QTextEdit.insertText()
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '种群信息导出完毕。\n')
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '最优的目标函数值为：%.8s mm\n' % (pvalue))
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '所在位置及相位偏斜角为：第%s级零件末端; %.8s°\n' % (find_index + 1 + n, res[find_index + n, 1]))
        if n == 0:
            for i in range(len(phase_list)):
                self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) +
                    '第%s级安装相位、偏心值及相位偏斜角为：%s°; %.8s mm; %.8s°\n' % (i + 1, phase_list[i], res[i, 0], res[i, 1]))
        else:
            for i in range(var_trace_shape_1):
                self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) +
                    '第%s级相位、偏心值及相位偏斜角为：%s°; %.8s mm; %.8s°\n' % (
                    i + (n + 1), phase_list[i + n], res[i + n, 0], res[i + n, 1]))
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '有效进化代数：%s\n' % (obj_trace_shape_0))
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '最优的一代是第 %s 代\n' % (best_gen + 1))
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '评价次数：%s\n' % (myAlgorithm_evalsNum))
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + f'时间已过 {int((end - start) // 60)} 分 {(end - start) % 60:.8f} 秒\n')
        self.cursor.insertText(str(time.strftime("%Y-%m-%d %H:%M:%S $ ")) + '==============================================================================\n')
        self.tab4.setTextCursor(self.cursor)
        self.tab4.ensureCursorVisible()

    def frame1_clear_predict(self):
        """
        清空预测结果
        """
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '清空预测结果')
        for line in [self.frame1_predict_value_line, self.frame1_predict_phase_line]:
            line.clear()

    def frame1_clear_optimize(self):
        """
        清空优化结果
        第二种方式添加图的清空（单张）
        """
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '清空优化结果')
        for line in [self.frame1_optimize_pvalue_line, self.frame1_optimize_value_line, self.frame1_optimize_phase_line]:
            line.clear()
        # 同时将self.phase清空
        self.phase = None
        if self.first_close != 0:
            self.frame2_p1.setData(x=[], y=[])
            self.frame2_ax.remove()
            self.frame2_ax = self.frame2_p2.fig.gca(projection='3d', title='等效模型', xlabel='x', ylabel='y')
            self.frame2_p2.draw()

    def frame1_clear_optimize_value_2(self):
        """
        清空优化结果
        第二种方式添加图的清空（多张）
        """
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '清空优化结果')
        for line in [self.frame1_optimize_pvalue_line, self.frame1_optimize_value_line, self.frame1_optimize_phase_line] + self.frame1_line_phase:
            line.clear()

    def frame1_clear_optimize_fig_2(self):
        """
        清空优化结果
        第二种方式添加图的清空（多张）
        """
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '清除图像')
        # 通过移除整个 item 实现清屏重绘(配合第二种图例添加方法)
        self.frame2_win1.removeItem(self.frame2_p1)
        self.frame2_p1 = self.frame2_win1.addPlot(row=0, col=0, title='遗传算法收敛图')
        self.frame2_p1.setLabel('left', "值")
        self.frame2_p1.setLabel('bottom', "进化代数")
        self.frame2_ax.remove()
        self.frame2_ax = self.frame2_p2.fig.gca(projection='3d', title='等效模型', xlabel='x', ylabel='y')
        self.frame2_p2.draw()

    def plot_objective_value(self):
        """
        绘制遗传算法的收敛图
        只能添加一张图
        """
        self.frame2_win1.removeItem(self.frame2_p1)
        self.frame2_p1 = self.frame2_win1.plot(x=self.gen, y=self.obj_trace, pen=pg.mkPen(color=(0,128,255), width=3, style=QtCore.Qt.SolidLine),
                                               name='种群最优个体目标值')

    def plot_objective_value_2(self):
        """
        绘制遗传算法的收敛图
        创建的窗口为 GraphicsLayoutWidget ，添加图的方式为 addPlot ,故可以添加多个图
        """
        # 通过移除整个 item 实现清屏重绘(配合第二种图例添加方法)
        self.frame2_win1.removeItem(self.frame2_p1)
        self.frame2_p1 = self.frame2_win1.addPlot(row=0, col=0, title='遗传算法收敛图')
        self.frame2_p1.setLabel('left', "值/mm")
        self.frame2_p1.setLabel('bottom', "进化代数")
        self.frame2_p1.plot(self.gen, self.obj_trace, pen=pg.mkPen(color=(0, 128, 255), width=3, style=QtCore.Qt.SolidLine), name='种群最优个体目标值')

        # 添加图例法二(图例内容可自定义)
        self.frame2_p1_plot = self.frame2_p1.plot(self.gen, self.obj_trace, pen=pg.mkPen(color=(0,128,255), width=3, style=QtCore.Qt.SolidLine), name='种群最优个体目标值')
        self.frame2_p1_legend = pg.LegendItem((100, 60), offset=(440, 30))      # 实例 LegendItem 对象, args are (size, offset)
        self.frame2_p1_legend.setParentItem(self.frame2_p1)   # 将其设为 self.frame2_p1 的子项
        self.frame2_p1_legend.addItem(self.frame2_p1_plot, '种群最优个体目标值')
        self.frame2_win1.show()

    def draw_figure(self, data):
        """
        绘制优化后 3D 示意图
        """
        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        self.frame2_ax.remove()
        self.frame2_ax = self.frame2_p2.fig.gca(projection='3d', title='等效模型', xlabel='x', ylabel='y')
        self.frame2_ax.plot(x, y, z, c='r', marker='o')
        for i in range(len(x)):
            x1 = np.linspace(-0.05 + x[i], 0.05 + x[i], 100)
            y1 = np.sqrt(abs(0.0025 - (x1 - x[i]) ** 2))
            z1 = np.array([z[i]] * 100)
            self.frame2_ax.plot(x1, y1 + y[i], z1, c='r')
            self.frame2_ax.plot(x1, -y1 + y[i], z1, c='r')
        self.frame2_p2.draw()  # 类似与 plt.show()，需要添加使其显示
        self.frame2_p2.flush_events()  # 重新绘图后刷新界面

    def show_predict_messagebox(self):
        """
        预测按钮提示框
        """
        if not self.h_default:
            QMessageBox.information(self, '提示', '请输入高度',QMessageBox.Ok)
        elif not self.r_default:
            QMessageBox.information(self, '提示', '请输入半径',QMessageBox.Ok)
        elif not self.phase:
            QMessageBox.information(self, '提示', '请输入安装相位',QMessageBox.Ok)

    def show_optimize_messagebox(self):
        """
        优化按钮提示框
        """
        if not self.h_default:
            QMessageBox.information(self, '提示', '请输入高度',QMessageBox.Ok)
        elif not self.r_default:
            QMessageBox.information(self, '提示', '请输入半径',QMessageBox.Ok)

    def update_time(self, s):
        """
        计时器更新时间，并通过 dialog_label 显示
        """
        s = s
        self.step += 1
        self.dialog_label.setText(str(f'正在{s}中，请稍等...{self.step / 10}s'))
        self.status_label.setText(str(f'正在{s}中，请稍等...{self.step / 10}s'))

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.consoleBox.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.consoleBox.setTextCursor(cursor)
        self.consoleBox.ensureCursorVisible()

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)


class Figure_Canvas(FigureCanvas):
    """
    定义一个新的类用来创建画板(基于 matplotlib 中的 Figure)
    """
    def __init__(self, parent=None, width=3.9, height=2.7, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=100)
        super(Figure_Canvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111, autoscale_on=True, visible=True)  # 打开坐标轴的自动缩放（也可以单独设置只缩放 x 或 y ）


class GAThread(QThread):
    # 自定义信号对象。参数 str 就代表这个信号可以传一个字符串，这里返回一个 list
    trigger = pyqtSignal(list)

    def __init__(self, runout, r, h):
        self.runout = runout
        self.r = r
        self.h = h
        # 初始化函数
        super(GAThread, self).__init__()

    def run(self):
        """
        重写线程执行的遗传算法主函数
        """
        Para_all = Para(self.runout, self.r)  # 注：此处不能写成Para = Para(..)，既不能同名
        para = Para_all.getPara2()
        aim = Stack_rigidity(self.runout, self.r, self.h, para)
        n = 0      # 累计的已固定好的级数
        Dim = len(self.h) - 1    # 初始决策变量维数(=总的级数-1)
        self.phase = None
        start = time.perf_counter()
        """===============================实例化问题对象==========================="""
        # PoolType = 'Thread'
        problem = MyProblem_aim3(aim, n, Dim, self.phase)  # 生成问题对象
        """=================================种群设置==============================="""
        Encoding = 'BG'  # 编码方式
        NIND = 1000  # 种群规模
        Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
        population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
        """===============================算法参数设置============================="""
        myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象
        # myAlgorithm.mutOper.Pm = 1 # 修改变异算子的变异概率(原模板中breeder GA变异算子的Pm定义为1 / Dim)
        # myAlgorithm.recOper.XOVR = 0.9 # 修改交叉算子的交叉概率
        # myAlgorithm.recOper.XOVR = 0.7 # 重组概率
        # myAlgorithm.mutOper.F = 0.5 # 差分进化中的参数F
        # if n == 0:
        #     myAlgorithm.MAXGEN = 20 # 最大进化代数
        #     myAlgorithm.maxTrappedCount = 10 # 进化停滞计数器最大上限值，如果连续maxTrappedCount代被判定进化陷入停滞，则终止进化
        # else:
        #     myAlgorithm.MAXGEN = 20
        myAlgorithm.MAXGEN = 40
        myAlgorithm.trappedValue = 1e-6  # “进化停滞”判断阈值
        myAlgorithm.maxTrappedCount = 10  # 进化停滞计数器最大上限值，如果连续maxTrappedCount代被判定进化陷入停滞，则终止进化
        myAlgorithm.drawing = 0  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
        """==========================调用算法模板进行种群进化======================="""
        [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板
        population.save()  # 把最后一代种群的信息保存到文件中
        # problem.pool.close() # 及时关闭问题类中的池，否则在采用多进程运算后内存得不到释放
        # 输出结果
        best_gen = np.argmin(problem.maxormins * obj_trace[:, 1])  # 记录最优种群个体是在哪一代
        best_ObjV = obj_trace[best_gen, 1]
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '==============================================================================')
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '种群信息导出完毕。')
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '最优的目标函数值为：%.8s mm' % (best_ObjV))
        if self.phase == None:
            self.phase = [0] + [i * 10 for i in var_trace[best_gen, :]]  # 第一次算出的所有相位值
            res = aim.bias_n_li_fast(self.phase)
            find_index = np.where(max(res[n + 1:, 0]) == res[n + 1:, 0])[0][
                             0] + 1  # 第一次最大偏心值的索引位置（此处res内的n+1和最后面的+1表示：不考虑第一级，整体向后偏移一位）
        else:
            self.phase = self.phase + [i * 10 for i in var_trace[best_gen, :]]  # 所有相位值(后续几级相位值有更新)
            res = aim.bias_n_li_fast(self.phase)
            find_index = np.where(max(res[n:, 0]) == res[n:, 0])[0][0]  # 每次的最大偏心值的索引位置
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '所在位置及相位偏斜角为：第%s级零件末端; %.8s°' % (find_index + 1 + n, res[find_index + n, 1]))

        op_list = []  # 将返回结果装入一个 list
        op_list.append(round(best_ObjV, 6))  # 0——投影偏心值
        op_list.append(round(res[-1, 0], 6))  # 1——偏心值
        op_list.append(round(res[find_index + n, 1], 4))  # 2——偏心相位
        op_list.append(find_index)  # 3——最优值索引位置
        op_list.append(n)  # 4——n
        op_list.append(res)  # 5——各级零件偏心结果res
        op_list.append(var_trace.shape[1])  # 6——var_trace.shape[1]

        if n == 0:
            for i in range(len(self.phase)):
                print(time.strftime("%Y-%m-%d %H:%M:%S $"), '第%s级安装相位、偏心值及相位偏斜角为：%s°; %.8s mm; %.8s°' % (i + 1, self.phase[i], res[i, 0], res[i, 1]))
        else:
            for i in range(var_trace.shape[1]):
                print(time.strftime("%Y-%m-%d %H:%M:%S $"),
                    '第%s级相位、偏心值及相位偏斜角为：%s°; %.8s mm; %.8s°' % (i + (n + 1), self.phase[i + n], res[i + n, 0], res[i + n, 1]))

        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '有效进化代数：%s' % (obj_trace.shape[0]))
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '最优的一代是第 %s 代' % (best_gen + 1))
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '评价次数：%s' % (myAlgorithm.evalsNum))
        n = n + int((find_index + 1))  # 计算累计固定好的级数(此处find_index类型为int64,改为int类型防止后面报错！)
        end = time.perf_counter()
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), f'时间已过 {int((end - start) // 60)} 分 {(end - start) % 60:.8f} 秒')
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '==============================================================================')

        self.gen = np.array([i for i in range(len(obj_trace))])  # 获取进化代数
        self.obj_trace = obj_trace[:, 1]                         # 每一代的最优目标值
        optimize_button_flag = 1

        op_list.append(self.phase)  # 7——优化得到的安装相位
        op_list.append(self.gen)  # 8——种群代数
        op_list.append(self.obj_trace)  # 9——目标函数值
        op_list.append(aim)  # 10——目标对象
        op_list.append(obj_trace.shape[0])  # 11——有效进化代数：obj_trace.shape[0]
        op_list.append(best_gen)  # 12——最优进化代数
        op_list.append(myAlgorithm.evalsNum)  # 13——评价次数
        op_list.append([start, end])  # 14——耗时
        op_list.append(optimize_button_flag)  # 15——传回标记
        # 通过自定义信号把待显示的字符串传递给槽函数
        self.trigger.emit(list(op_list))


class PRThread(QThread):
    trigger = pyqtSignal(list)

    def __init__(self, runout, r, h, phase):
        self.runout = runout
        self.r = r
        self.h = h
        self.phase = phase
        super(PRThread, self).__init__()

    def run(self):
        """
        重写线程的精度预测主函数
        """
        start = time.perf_counter()
        Para_all = Para(self.runout, self.r)  # 注：此处不能写成Para = Para(..)，既不能同名
        para = Para_all.getPara2()
        aim = Stack_rigidity(self.runout, self.r, self.h, para)
        res = aim.bias_n_li_fast(self.phase)
        end = time.perf_counter()
        value = round(res[-1, 0], 6)
        phase = round(res[-1, 1], 4)
        phase_list = self.phase
        predict_button_flag = 1

        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '==============================================================================')
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '预测偏心值为：%s mm' % value)
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '预测偏心相位为：%s°' % phase)
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), f'时间已过 {int((end - start) // 60)} 分 {(end - start) % 60:.8f} 秒')
        print(time.strftime("%Y-%m-%d %H:%M:%S $"), '==============================================================================')

        pr_list = []
        pr_list.append(value)  # 0——种群代数
        pr_list.append(phase)  # 1——优化得到的安装相位
        pr_list.append(phase_list)  #2——安装相位
        pr_list.append(aim)  # 3——目标对象
        pr_list.append(predict_button_flag)  # 4——传回标记
        pr_list.append([start, end])  # 5——耗时
        # 通过自定义信号把待显示的字符串传递给槽函数
        self.trigger.emit(list(pr_list))


class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash = QSplashScreen()
    splash.setPixmap(QPixmap('images/splash.jpg'))
    splash.show()
    splash.showMessage('Welcome to Use This PyQt5-Made Software~',
                       QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.white)

    ui = Ui_MainWindow()
    ui.show()
    splash.finish(ui)

    sys.exit(app.exec_())







"""
上一版本：软件0.2
改变及增加内容：
1. 将 Demo 合并到主界面 MainWindow 中; 状态栏添加优化实时耗时
2. 为防止界面假死，将预测和优化的主函数写入另外的新的线程执行，同时在状态栏实时显示耗时
3. 此版本无法动态显示遗传算法的收敛过程，因为报错：signal only works in main thread(signal只能工作在主线程中),是由于2新建了一个线程。
4. 现存问题：绘制收敛图时，若使用第一种图例添加方法，首次绘图图例不显示。
解决：使用第二种添加方法，且清屏时将整个 Item 全部清除而不是只 clearPlots。(注：有时可能会出现残留上一张图像边缘的问题)
5. 预测和优化按钮均添加了 flag 标记，防止多次点击重复运行（运行时 flag 置为0，单次运行完毕后 flag 置为1）
6. 添加背景图片
7. 将计算结果输出到 tab4——textedit 控件中，将控制台输出添加到 consolebox 中
8. 为 tab4 添加记事本功能
9. 预测和优化时设置子窗口置顶
"""

