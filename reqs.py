def startup():
	global win,p1,inp,FRAME,RED,BLUE,BLACK
	from game import win, p1, inp, FRAME, RED, BLUE, BLACK

def startupScreen(win):
	pass

def selectionScreen(sel, header, hcolor=(255,0,0)):
	global win, p1, inp, FRAME, RED, BLUE, BLACK
	selected = 1
	print sel
	while True:
		FRAME+=1 #Count this as a frame broski!
		win.fill(bgcolor=BLACK)
		win.putchars(header, 1, 1, fgcolor=hcolor)
		if len(sel.keys()) > 1:
			for i in xrange(1, len(sel.keys())):
				line = '[%s] %s' % (i, sel[i])
				if i == selected: win.putchars(line, 1, i+1, fgcolor=RED, bgcolor=BLUE)
				else: win.putchars(line, 1, i+1, fgcolor=RED)
			win.update()
		else:
			win.fill(bgcolor=BLACK)
			line = '[%s] %s' % (1, sel[1])
			win.putchars(line, 1, 2, fgcolor=RED, bgcolor=BLUE)
			win.update()
		val = inp.mwaitFor(['w','s','enter'])
		if val == 'w' and selected >= 2:
			selected -= 1
		elif val == 's' and selected < len(sel.keys())-1:
			selected += 1
		elif val == 'enter':
			return selected

eatMessage = ['Om nom nom! Tis a good %s',
'You eat the %s like a boss...',
'You tear the %s apart, shoving pieces in your mouth',
'RARR! Gooooood %s']