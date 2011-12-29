def startup():
	global win,p1,inp,FRAME,RED,BLUE,BLACK
	from game import win, p1, inp, FRAME, RED, BLUE, BLACK

def startupScreen(win):
	pass

def selectionScreen(sel):
	global win, p1, inp, FRAME, RED, BLUE, BLACK
	selected = 1
	while True:
		FRAME+=1 #Count this as a frame broski!
		win.fill(bgcolor=BLACK)
		for i in xrange(1, len(sel.keys())):
			line = '[%s] %s' % (i, sel[i])
			if i == selected:
				win.putchars(line, 1, i+1, fgcolor=RED, bgcolor=BLUE)
			else:
				win.putchars(line, 1, i+1, fgcolor=RED)
		win.update()
		val = inp.mwaitFor(['w','s','enter'])
		if val == 'w' and selected >= 2:
			selected -= 1
		elif val == 's' and selected <= len(sel.keys())-2:
			selected += 1
		elif val == 'enter':
			return selected