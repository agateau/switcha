#ifndef WINDOW_H
#define WINDOW_H

// Qt
#include <qwidget.h>

// KDE
#include <kwin.h>

class QCloseEvent;
class QListViewItem;
class QEvent;
class KListView;
class KListViewSearchLine;

class Window : public QWidget {
	Q_OBJECT
public:
	Window();

public slots:
	void showAgain();

protected:
	virtual bool eventFilter(QObject*, QEvent*);

	virtual void closeEvent(QCloseEvent*);

private slots:
	void switchToWindow(QListViewItem*);
	void slotReturnPressed();

private:
	void updateWindowInfoList();

	typedef QValueList<KWin::WindowInfo> WindowInfoList;
	WindowInfoList mWindowInfoList;
	KListViewSearchLine* mLineEdit;
	KListView* mView;
};

#endif /* WINDOW_H */
