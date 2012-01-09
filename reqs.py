import time, string
from pygame.locals import *
def startup():
	global win,p1,inp,FRAME,RED,BLUE,BLACK
	from game import win, p1, inp, FRAME, RED, BLUE, BLACK

trade = lambda x,y: (y,x)

def startupScreen(win):
	pass

def sdisplay(text):
	win.fill(bgcolor=BLACK)
	win.putchars(text, 1, 1)
	win.update()

def ask(question):
	current_string = []
	sdisplay(question + ": " + string.join(current_string,""))
	while 1:
		inkey = inp.simpleRet()
		if inkey == K_BACKSPACE:
		  current_string = current_string[0:-1]
		elif inkey == K_RETURN:
		  break
		elif inkey == K_MINUS:
		  current_string.append("_")
		elif inkey <= 127:
		  current_string.append(chr(inkey))
		sdisplay(question + ": " + string.join(current_string,""))
	return string.join(current_string,"")

def selectionScreen(sel, header, hcolor=(255,0,0), footer='', fcolor=(255,0,0), removeable=False, niceremove=True):
	global win, p1, inp, FRAME, RED, BLUE, BLACK
	selected = 1
	valy = 1
	deld = []
	print sel
	while True:
		FRAME+=1 #Count this as a frame broski!
		win.fill(bgcolor=BLACK)
		win.putchars(header, 1, 1, fgcolor=hcolor)
		if len(sel.keys()) > 1:
			for i in xrange(0, len(sel.keys())):
				line = '[%s] %s' % (i+1, sel[i+1])
				if i+1 == selected: win.putchars(line, 1, i+1, fgcolor=RED, bgcolor=BLUE)
				else: win.putchars(line, 1, i+1, fgcolor=RED)
				valy += 1
		else:
			win.fill(bgcolor=BLACK)
			line = '[%s] %s' % (1, sel[1])
			win.putchars(line, 1, 2, fgcolor=RED, bgcolor=BLUE)
			valy = 3
		win.putchars(footer, 1, valy, fgcolor=fcolor)
		win.update()
		val = inp.mwaitFor(['w','s','enter', 'r', 'q'])
		if val == 'w' and selected >= 2:
			selected -= 1
		elif val == 's' and selected < len(sel.keys()):
			selected += 1
		elif val == 'r':
			if niceremove is True:
				sel[selected] = 'Empty!'
			else:
				del sel[selected]
			deld.append(selected)
			print len(sel)
			if len(sel) == 0:
				return (selected, deld)
		elif val == 'enter':
			return (selected, deld)
		elif val == 'q':
			return (None, None)
		valy = 1

eatMessage = ['Om nom nom! Tis a good %s',
'You eat the %s like a boss...',
'You tear the %s apart, shoving pieces in your mouth',
'RARR! Gooooood %s']