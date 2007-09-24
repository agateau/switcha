#!/usr/bin/env python
import os
import sys
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *

reSimplify = re.compile("  +")
def simplifySpaces(txt):
	return reSimplify.sub(" ", txt)


def runWmCtrl(*args):
	cmd = ["wmctrl"]
	cmd.extend(args)
	print cmd
	sin, sout = os.popen2(cmd)
	sin.close()
	lines = [simplifySpaces(x.strip()) for x in sout.readlines()]
	return lines


def getWindowList():
	"""0x032000e1  0 cpc6128 Qt Designer"""
	lines = runWmCtrl("-l")
	lst = []
	for line in lines:
		tokens = line.split(" ")
		wid = tokens[0]
		text = " ".join(tokens[3:])
		lst.append( (text, wid) )
	return lst


def switchToWindow(wid):
	runWmCtrl("-ia", wid)


class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.initModel()
		self.initView()


	def initModel(self):
		lst = getWindowList()
		self._model = QStandardItemModel()
		for text, wid in lst:
			item = QStandardItem(unicode(text, "utf8"))
			data = QVariant(QString(wid))
			item.setData(data)
			self._model.appendRow(item)


	def initView(self):
		self._view = QListView(self)
		layout = QVBoxLayout(self)
		layout.setMargin(0)
		layout.addWidget(self._view)
		self._view.setModel(self._model)
		self._view.setEditTriggers(QAbstractItemView.NoEditTriggers)

		QObject.connect(self._view, SIGNAL("activated(const QModelIndex&)"),
			self.switchToWindow)

	def switchToWindow(self, index):
		item = self._model.itemFromIndex(index)
		wid = item.data().toString()
		switchToWindow(unicode(wid))
		self.close()

def main():
	app = QApplication(sys.argv)
	window = Window()

	window.show()
	window.resize(400, 300)
	app.exec_()


if __name__=="__main__":
	main()
