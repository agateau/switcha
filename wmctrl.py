import os
import re

BLACKLIST=[
"KDE Desktop",
"kicker"
]

reSimplify = re.compile("  +")
def simplifySpaces(txt):
	return reSimplify.sub(" ", txt)


def runWmCtrl(*args):
	cmd = ["wmctrl"]
	cmd.extend(args)
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
		if text not in BLACKLIST:
			lst.append( (text, wid) )
	return lst


def switchToWindow(wid):
	runWmCtrl("-ia", wid)
