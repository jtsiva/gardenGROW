import sys

from PyQt4 import QtCore, QtGui
from form import Ui_mainWindow
import pyqtgraph as pg
import math
 
class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.comboBox.addItem("Dawn-Dusk Scheduler")
        self.ui.comboBox.addItem("As-needed Scheduler")
        self.ui.comboBox.addItem("Advanced Scheduler")


def main ():
	app = QtGui.QApplication(sys.argv)
	myapp = MyWindow()

	rmsData = []
	cmsData = []
	tempData = []
	lightData = []
	waterData = []
	schedulerData = []
	xData = []

	with open("data/0-CMS.txt") as f:
		for line in f:
			cmsData.append (int(line.split(",")[0]))
			xData.append (line.split(",")[1])
	myapp.ui.cms_plot.plot(cmsData)
	xData = []

	with open("data/0-RMS.txt") as f:
		for line in f:
			rmsData.append (int(line.split(",")[0]))
			xData.append (line.split(",")[1])
	myapp.ui.rms_plot.plot(rmsData)
	xData = []

	with open("data/0-light.txt") as f:
		for line in f:
			lightData.append (int(line.split(",")[0]))
			xData.append (line.split(",")[1])
	myapp.ui.daylight_plot.plot(lightData)
	xData = []

	with open("data/0-temp.txt") as f:
		for line in f:
			tempData.append (int(line.split(",")[0]))
			xData.append (line.split(",")[1])
	myapp.ui.temp_plot.plot(tempData)
	xData = []

	with open("data/waterUsed.txt") as f:
		total = 0
		for line in f:
			total += int(line.split(",")[0])
			waterData.append (total)
			xData.append (line.split(",")[1])
	myapp.ui.water_use_plot.plot(waterData)
	xData = []

	schedule = [0 for i in xrange(48)]
	if str(myapp.ui.comboBox.currentText()) == "Dawn-Dusk Scheduler":
		schedule[12] = 1
		schedule[38] = 1
	elif str(myapp.ui.comboBox.currentText()) == "As-needed Scheduler":
		for i in range(3,12):
			schedule[i] = .08 * i
			schedule[i+30] = .08 * i
	else:
		for i in range(0,48):
			schedule[i] = i * (2 * PI) / 48.0	

	myapp.ui.watering_chance_plot.plot(schedule)

	myapp.show()
	sys.exit(app.exec_())
 
if __name__ == "__main__":
	main()
        