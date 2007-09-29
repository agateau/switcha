#include "window.moc"

// Qt
#include <qevent.h>
#include <qheader.h>
#include <qlayout.h>

// KDE
#include <klistview.h>
#include <klistviewsearchline.h>
#include <klocale.h>
#include <krun.h>
#include <kwinmodule.h>


/**
 * Subclass KListViewSearchLine to select the first visible item if the
 * previous selected item gets filtered out
 */
class ListViewSearchLine : public KListViewSearchLine {
public:
	ListViewSearchLine(QWidget* parent)
	: KListViewSearchLine(parent) {}


	void updateSearch(const QString& text) {
		KListViewSearchLine::updateSearch(text);

		KListView* view = listView();
		QListViewItem* item = view->selectedItem();
		if (item && item->isVisible()) {
			return;
		}

		QListViewItemIterator iterator(view, QListViewItemIterator::Visible);
		item = iterator.current();
		if (item) {
			view->setSelected(item, true);
		}
	}
};


Window::Window()
: QDialog(0) {
	setCaption(i18n("Switcha"));

	// Line edit
	mLineEdit = new ListViewSearchLine(this);
	connect(mLineEdit, SIGNAL(returnPressed()), SLOT(slotReturnPressed()) );
	mLineEdit->installEventFilter(this);

	// View
	mView = new KListView(this);
	mView->header()->hide();
	mView->addColumn("");
	mView->setResizeMode(QListView::LastColumn);
	connect(mView, SIGNAL(clicked(QListViewItem*)), SLOT(switchToWindow(QListViewItem*)) );

	mLineEdit->setListView(mView);

	// Layout
	QVBoxLayout* layout = new QVBoxLayout(this);
	layout->setMargin(6);
	layout->setSpacing(6);
	layout->addWidget(mLineEdit);
	layout->addWidget(mView);
}


void Window::closeEvent(QCloseEvent* event) {
	hide();
	event->ignore();
}


void Window::showAgain() {
	mLineEdit->clear();
	mView->clear();

	updateWindowInfoList();

	WindowInfoList::ConstIterator
		it = mWindowInfoList.begin(),
		end = mWindowInfoList.end();
	
	for (; it!=end; ++it) {
		KWin::WindowInfo info = *it;
		QListViewItem* item = new QListViewItem(mView, info.visibleName());
		QPixmap pix = KWin::icon(info.win(), 16, 16, true);
		item->setPixmap(0, pix);
	}

	if (!mWindowInfoList.empty()) {
		mView->setSelected(mView->firstChild(), true);
	}

	QRect rect = QApplication::desktop()->availableGeometry();
	int width = mView->columnWidth(0) + 30;
	int height = 300;
	move(
		rect.left() + (rect.width() - width) / 2,
		rect.top() + (rect.height() - height) / 2
		);
	resize(width, height);
	show();
	KWin::forceActiveWindow(winId());
}


void Window::updateWindowInfoList() {
	KWinModule kwinModule;
	typedef QValueList<WId> WIdList;
	const WIdList & list = kwinModule.windows();

	WIdList::ConstIterator
		it = list.begin(),
		end = list.end();

	mWindowInfoList.clear();
	for (; it!=end; ++it) {
		KWin::WindowInfo info = KWin::windowInfo(*it);
		NET::WindowType type = info.windowType(NET::AllTypesMask);
		if (type != NET::Desktop && type != NET::Dock && type != NET::Menu) {
			mWindowInfoList << info;
		}
	}
}


bool Window::eventFilter(QObject*, QEvent* event) {
	if (event->type() != QEvent::KeyPress) {
		return false;
	}

	QKeyEvent* keyEvent = static_cast<QKeyEvent*>(event);
	if (keyEvent->key() == Qt::Key_Up || keyEvent->key() == Qt::Key_Down) {
		QKeyEvent* newEvent = new QKeyEvent(
			keyEvent->type(), keyEvent->key(), keyEvent->ascii(),
			keyEvent->state(), keyEvent->text());
		QApplication::postEvent(mView, newEvent);
		return true;
	}

	return false;
}


void Window::switchToWindow(QListViewItem* item) {
	QString itemName = item->text(0);

	WindowInfoList::ConstIterator
		it = mWindowInfoList.begin(),
		end = mWindowInfoList.end();
	
	for (; it!=end; ++it) {
		KWin::WindowInfo info = *it;
		if (info.visibleName() == itemName) {
			hide();
			KWin::forceActiveWindow(info.win());
			return;
		}
	}
}

void Window::slotReturnPressed() {
	QListViewItem* item = mView->selectedItem();
	if (item && item->isVisible()) {
		switchToWindow(item);
	} else {
		QString cmd = mLineEdit->text();
		KRun::runCommand(cmd);
		hide();
	}
}
