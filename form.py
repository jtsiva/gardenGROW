# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(665, 646)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.forecastW_slider = QtGui.QSlider(self.centralwidget)
        self.forecastW_slider.setGeometry(QtCore.QRect(110, 490, 160, 40))
        self.forecastW_slider.setOrientation(QtCore.Qt.Horizontal)
        self.forecastW_slider.setObjectName(_fromUtf8("forecastW_slider"))
        self.water_slider = QtGui.QSlider(self.centralwidget)
        self.water_slider.setGeometry(QtCore.QRect(110, 530, 160, 29))
        self.water_slider.setOrientation(QtCore.Qt.Horizontal)
        self.water_slider.setObjectName(_fromUtf8("water_slider"))
        self.waterLimit_slider = QtGui.QSlider(self.centralwidget)
        self.waterLimit_slider.setGeometry(QtCore.QRect(110, 570, 160, 20))
        self.waterLimit_slider.setOrientation(QtCore.Qt.Horizontal)
        self.waterLimit_slider.setObjectName(_fromUtf8("waterLimit_slider"))
        self.randOp_slider = QtGui.QSlider(self.centralwidget)
        self.randOp_slider.setGeometry(QtCore.QRect(430, 490, 160, 29))
        self.randOp_slider.setOrientation(QtCore.Qt.Horizontal)
        self.randOp_slider.setObjectName(_fromUtf8("randOp_slider"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 460, 671, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(8, 500, 101, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(9, 534, 101, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(9, 567, 81, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(328, 495, 110, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.cms_plot = PlotWidget(self.centralwidget)
        self.cms_plot.setGeometry(QtCore.QRect(20, 70, 291, 111))
        self.cms_plot.setObjectName(_fromUtf8("cms_plot"))
        self.temp_plot = PlotWidget(self.centralwidget)
        self.temp_plot.setGeometry(QtCore.QRect(20, 200, 291, 111))
        self.temp_plot.setObjectName(_fromUtf8("temp_plot"))
        self.water_use_plot = PlotWidget(self.centralwidget)
        self.water_use_plot.setGeometry(QtCore.QRect(20, 340, 291, 111))
        self.water_use_plot.setObjectName(_fromUtf8("water_use_plot"))
        self.rms_plot = PlotWidget(self.centralwidget)
        self.rms_plot.setGeometry(QtCore.QRect(350, 70, 291, 111))
        self.rms_plot.setObjectName(_fromUtf8("rms_plot"))
        self.daylight_plot = PlotWidget(self.centralwidget)
        self.daylight_plot.setGeometry(QtCore.QRect(350, 200, 291, 111))
        self.daylight_plot.setObjectName(_fromUtf8("daylight_plot"))
        self.rain_chance_plot = PlotWidget(self.centralwidget)
        self.rain_chance_plot.setGeometry(QtCore.QRect(350, 340, 291, 111))
        self.rain_chance_plot.setObjectName(_fromUtf8("rain_chance_plot"))
        self.test_button = QtGui.QPushButton(self.centralwidget)
        self.test_button.setGeometry(QtCore.QRect(330, 540, 89, 27))
        self.test_button.setObjectName(_fromUtf8("test_button"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(160, 20, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 665, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "Garden GROW Dashboard", None))
        self.label.setText(_translate("mainWindow", "Forecast Weight", None))
        self.label_2.setText(_translate("mainWindow", "Water threshold", None))
        self.label_3.setText(_translate("mainWindow", "Water Limit", None))
        self.label_4.setText(_translate("mainWindow", "Random Option", None))
        self.test_button.setText(_translate("mainWindow", "Test", None))
        self.label_5.setText(_translate("mainWindow", "Garden GROW Dashboard", None))

from pyqtgraph import PlotWidget
