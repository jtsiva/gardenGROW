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
        self.forecastW_slider.setGeometry(QtCore.QRect(140, 490, 160, 40))
        self.forecastW_slider.setOrientation(QtCore.Qt.Horizontal)
        self.forecastW_slider.setObjectName(_fromUtf8("forecastW_slider"))
        self.water_slider = QtGui.QSlider(self.centralwidget)
        self.water_slider.setGeometry(QtCore.QRect(140, 530, 160, 29))
        self.water_slider.setOrientation(QtCore.Qt.Horizontal)
        self.water_slider.setObjectName(_fromUtf8("water_slider"))
        self.waterLimit_slider = QtGui.QSlider(self.centralwidget)
        self.waterLimit_slider.setGeometry(QtCore.QRect(140, 570, 160, 20))
        self.waterLimit_slider.setOrientation(QtCore.Qt.Horizontal)
        self.waterLimit_slider.setObjectName(_fromUtf8("waterLimit_slider"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 470, 671, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(8, 500, 111, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(9, 534, 111, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(9, 567, 81, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.cms_plot = PlotWidget(self.centralwidget)
        self.cms_plot.setGeometry(QtCore.QRect(20, 70, 291, 111))
        self.cms_plot.setObjectName(_fromUtf8("cms_plot"))
        self.temp_plot = PlotWidget(self.centralwidget)
        self.temp_plot.setGeometry(QtCore.QRect(20, 210, 291, 111))
        self.temp_plot.setObjectName(_fromUtf8("temp_plot"))
        self.water_use_plot = PlotWidget(self.centralwidget)
        self.water_use_plot.setGeometry(QtCore.QRect(20, 350, 291, 111))
        self.water_use_plot.setObjectName(_fromUtf8("water_use_plot"))
        self.rms_plot = PlotWidget(self.centralwidget)
        self.rms_plot.setGeometry(QtCore.QRect(350, 70, 291, 111))
        self.rms_plot.setObjectName(_fromUtf8("rms_plot"))
        self.daylight_plot = PlotWidget(self.centralwidget)
        self.daylight_plot.setGeometry(QtCore.QRect(350, 210, 291, 111))
        self.daylight_plot.setObjectName(_fromUtf8("daylight_plot"))
        self.watering_chance_plot = PlotWidget(self.centralwidget)
        self.watering_chance_plot.setGeometry(QtCore.QRect(350, 350, 291, 111))
        self.watering_chance_plot.setObjectName(_fromUtf8("watering_chance_plot"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(160, 10, 411, 31))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(350, 490, 291, 30))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 50, 191, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(350, 50, 181, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 190, 91, 17))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(350, 190, 67, 17))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 330, 91, 17))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(350, 330, 161, 17))
        self.label_10.setObjectName(_fromUtf8("label_10"))
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
        self.label_5.setText(_translate("mainWindow", "Garden GROW Dashboard", None))
        self.label_4.setText(_translate("mainWindow", "Capacitive Moisture Sensor", None))
        self.label_6.setText(_translate("mainWindow", "Resistive Moisture Sensor", None))
        self.label_7.setText(_translate("mainWindow", "Temperature", None))
        self.label_8.setText(_translate("mainWindow", "Light", None))
        self.label_9.setText(_translate("mainWindow", "Water Usage", None))
        self.label_10.setText(_translate("mainWindow", "Watering Schedule", None))

from pyqtgraph import PlotWidget
