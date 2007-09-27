#!/usr/bin/env python
import os
import sys

from qt import *
from kdecore import *
from kdeui import *


class ListViewSearchLine(KListViewSearchLine):
	def updateSearch(self, text):
		KListViewSearchLine.updateSearch(self, text)

		view = self.listView()
		item = view.selectedItem()
		if item and item.isVisible():
			return

		iterator = QListViewItemIterator(view, QListViewItemIterator.Visible)
		item = iterator.current()
		if item:
			view.setSelected(item, True)


class Window(QDialog):
	def __init__(self):
		QDialog.__init__(self)
		self.setCaption("Switcha")
		self.initModel()
		self.initUi()


	def initModel(self):
		kwinModule = KWinModule()
		self._windowList = []
		for wid in kwinModule.windows():
			info = KWin.windowInfo(wid)
			windowType = info.windowType(NET.AllTypesMask)
			if windowType not in (NET.Desktop, NET.Dock, NET.Menu):
				self._windowList.append(info)


	def initUi(self):
		frame = QFrame(self)
		frame.setFrameStyle(QFrame.Box | QFrame.Plain)
		layout = QVBoxLayout(self)
		layout.setMargin(0)
		layout.addWidget(frame)

		# LineEdit
		self._lineEdit = ListViewSearchLine(frame)
		QObject.connect(self._lineEdit, SIGNAL("returnPressed()"),
			self.slotReturnPressed)

		self._lineEdit.installEventFilter(self)

		# View
		self._view = KListView(frame)
		self._view.addColumn("")
		self._view.header().hide()
		for info in self._windowList:
			QListViewItem(self._view, info.visibleName())

		if len(self._windowList) > 0:
			self._view.setSelected(self._view.firstChild(), True)

		QObject.connect(self._view, SIGNAL("clicked(QListViewItem*)"),
			self.switchToWindow)

		self._lineEdit.setListView(self._view)

		# Layout
		layout = QVBoxLayout(frame)
		layout.setMargin(6)
		layout.addWidget(self._lineEdit)
		layout.addWidget(self._view)


	def slotCurrentChanged(self, item):
		if not item:
			self.selectFirstItem()


	def eventFilter(self, obj, event):
		if event.type() != QEvent.KeyPress:
			return False

		if event.key() in (Qt.Key_Up, Qt.Key_Down):
			newEvent = QKeyEvent(event.type(), event.key(), event.ascii(), event.state(), event.text())
			QApplication.postEvent(self._view, newEvent)
			return True

		return False


	def switchToWindow(self, item):
		itemName = item.text(0)
		for info in self._windowList:
			if info.visibleName() == itemName:
				KWin.forceActiveWindow(info.win())
				self.close()
				return


	def slotReturnPressed(self):
		item = self._view.selectedItem()
		if item and item.isVisible():
			self.switchToWindow(item)
		else:
			cmd = unicode(self._lineEdit.text())
			os.spawnlp(os.P_NOWAIT, 'sh', 'sh', '-c', cmd)
			self.close()


def main():
	# Keep app global otherwise there is a crash on exit
	global app
	description = "A fast window switcher and application launcher"
	version     = "1.0"
	aboutData   = KAboutData ("", "",\
		version, description, KAboutData.License_GPL,\
		"(C) 2007 Aurelien Gateau")
	KCmdLineArgs.init (sys.argv, aboutData)

	app = KApplication()
	window = Window()

	rect = QApplication.desktop().availableGeometry()
	window.move( \
		rect.left() + (rect.width() - window.sizeHint().width()) / 2, \
		rect.top() + (rect.height() - window.sizeHint().height()) / 2 \
		)
	window.exec_loop()


if __name__ == "__main__":
	main()
