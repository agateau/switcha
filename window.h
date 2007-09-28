#ifndef WINDOW_H
#define WINDOW_H

// Qt
#include <qdialog.h>

// KDE
#include <kwin.h>

class QListViewItem;
class QEvent;
class KListView;
class KListViewSearchLine;

class Window : public QDialog {
	Q_OBJECT
public:
	Window();


protected:
	virtual bool eventFilter(QObject*, QEvent*);

private slots:
	void switchToWindow(QListViewItem*);
	void slotReturnPressed();

private:
	void initList();
	void initUi();

	typedef QValueList<KWin::WindowInfo> WindowInfoList;
	WindowInfoList mWindowInfoList;
	KListViewSearchLine* mLineEdit;
	KListView* mView;
};

#endif /* WINDOW_H */
