// Local
#include "window.h"

// Qt
#include <qlabel.h>

// KDE
#include <kaboutdata.h>
#include <kapplication.h>
#include <kcmdlineargs.h>

int main(int argc, char** argv) {
	KAboutData aboutData("switcha", I18N_NOOP("Switcha"),
		"1.0", I18N_NOOP("A fast window switcher and application launcher"), KAboutData::License_GPL,
		"Copyright 2007, Aurélien Gâteau", 0, 0);

	KCmdLineArgs::init(argc, argv, &aboutData);
	KApplication kapplication;

	Window window;
	QRect rect = QApplication::desktop()->availableGeometry();
	window.move(
		rect.left() + (rect.width() - window.sizeHint().width()) / 2,
		rect.top() + (rect.height() - window.sizeHint().height()) / 2
		);
	window.show();
	kapplication.setMainWidget(&window);

	return kapplication.exec();
}
