// Local
#include "window.h"

// KDE
#include <kaboutdata.h>
#include <kapplication.h>
#include <kcmdlineargs.h>
#include <kglobalaccel.h>
#include <ksystemtray.h>

int main(int argc, char** argv) {
	KAboutData aboutData("switcha", I18N_NOOP("Switcha"),
		"1.0", I18N_NOOP("A fast window switcher and application launcher"), KAboutData::License_GPL,
		"Copyright 2007, Aurélien Gâteau", 0, 0);

	KCmdLineArgs::init(argc, argv, &aboutData);
	KApplication kapplication;

	Window window;
	kapplication.setMainWidget(&window);

	KSystemTray tray(&window);
	tray.show();

	KGlobalAccel accel(&window);
	accel.insert("show", i18n("Show"),
		i18n("Show Switcha window"),
		Qt::ALT + Qt::Key_F5, 0, &window, SLOT(showAgain()) );
	accel.updateConnections();

	return kapplication.exec();
}
