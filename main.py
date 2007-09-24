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


class ListView(QListView):
	def sizeHint(self):
		width = 0
		height = 0
		options = self.viewOptions()
		for pos in range(self.model().rowCount()):
			index = self.model().index(pos, 0)
			hint = self.itemDelegate().sizeHint(options, index)
			width = max(width, hint.width())
			height += hint.height()
		return QSize(width + 10, height + 10)


class Window(QDialog):
	def __init__(self):
		QDialog.__init__(self)
		self.initModel()
		self.initProxyModel()
		self.initView()


	def initModel(self):
		lst = getWindowList()
		self._model = QStandardItemModel()
		for text, wid in lst:
			item = QStandardItem(unicode(text, "utf8"))
			data = QVariant(QString(wid))
			item.setData(data)
			self._model.appendRow(item)


	def initProxyModel(self):
		self._proxyModel = QSortFilterProxyModel()
		self._proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
		self._proxyModel.setSourceModel(self._model)


	def initView(self):
		# LineEdit
		self._lineEdit = QLineEdit(self)
		QObject.connect(self._lineEdit, SIGNAL("textEdited(const QString&)"),
			self.updateFilter)
		QObject.connect(self._lineEdit, SIGNAL("returnPressed()"),
			self.slotReturnPressed)

		self._lineEdit.installEventFilter(self)

		# View
		self._view = ListView(self)
		self._view.setModel(self._proxyModel)
		self._view.setEditTriggers(QAbstractItemView.NoEditTriggers)
		QObject.connect(self._view, SIGNAL("activated(const QModelIndex&)"),
			self.switchToWindow)

		# Layout
		layout = QVBoxLayout(self)
		layout.setMargin(0)
		layout.addWidget(self._lineEdit)
		layout.addWidget(self._view)


	def updateFilter(self, text):
		self._proxyModel.setFilterFixedString(text)
		if not self._view.currentIndex().isValid():
			firstIndex = self._proxyModel.index(0, 0)
			if firstIndex.isValid():
				self._view.setCurrentIndex(firstIndex)


	def eventFilter(self, obj, event):
		if event.type() != QEvent.KeyPress:
			return False

		if event.key() in (Qt.Key_Up, Qt.Key_Down):
			newEvent = QKeyEvent(event.type(), event.key(), event.modifiers(), event.text())
			QApplication.postEvent(self._view, newEvent)
			return True

		return False


	def switchToWindow(self, index):
		sourceIndex = self._proxyModel.mapToSource(index)
		item = self._model.itemFromIndex(sourceIndex)
		wid = item.data().toString()
		switchToWindow(unicode(wid))
		self.close()


	def slotReturnPressed(self):
		index = self._view.currentIndex()
		if index.isValid():
			self.switchToWindow(index)
		else:
			cmd = unicode(self._lineEdit.text())
			os.spawnlp(os.P_NOWAIT, 'sh', 'sh', '-c', cmd)
			self.close()


def main():
	app = QApplication(sys.argv)
	window = Window()

	rect = QApplication.desktop().availableGeometry()
	window.move( \
		rect.left() + (rect.width() - window.sizeHint().width()) / 2, \
		rect.top() + (rect.height() - window.sizeHint().height()) / 2 \
		)
	window.show()
	app.exec_()


if __name__=="__main__":
	main()
