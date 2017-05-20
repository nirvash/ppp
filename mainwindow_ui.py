# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\face\ppp\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(867, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cascadeFilepath = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cascadeFilepath.sizePolicy().hasHeightForWidth())
        self.cascadeFilepath.setSizePolicy(sizePolicy)
        self.cascadeFilepath.setDragEnabled(False)
        self.cascadeFilepath.setObjectName("cascadeFilepath")
        self.verticalLayout.addWidget(self.cascadeFilepath)
        self.imageFilepath = QtWidgets.QLineEdit(self.centralwidget)
        self.imageFilepath.setObjectName("imageFilepath")
        self.verticalLayout.addWidget(self.imageFilepath)
        self.graphicsView = RubberBandGraphicsView(self.centralwidget)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setAcceptDrops(False)
        self.graphicsView.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.graphicsView.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(75, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonLeft = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLeft.sizePolicy().hasHeightForWidth())
        self.pushButtonLeft.setSizePolicy(sizePolicy)
        self.pushButtonLeft.setObjectName("pushButtonLeft")
        self.horizontalLayout.addWidget(self.pushButtonLeft)
        self.pushButtonRight = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRight.setObjectName("pushButtonRight")
        self.horizontalLayout.addWidget(self.pushButtonRight)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonAction = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAction.sizePolicy().hasHeightForWidth())
        self.pushButtonAction.setSizePolicy(sizePolicy)
        self.pushButtonAction.setObjectName("pushButtonAction")
        self.horizontalLayout.addWidget(self.pushButtonAction)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 867, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ppp"))
        self.pushButtonLeft.setText(_translate("MainWindow", "<"))
        self.pushButtonRight.setText(_translate("MainWindow", ">"))
        self.pushButtonAction.setText(_translate("MainWindow", "Action"))

from RubberBandGraphicsView import RubberBandGraphicsView
