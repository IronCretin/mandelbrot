# usage: python mandelbrot.py <power> <display x> < display y> <max recursion> <center x> <center y> <width x> <width y> <file name>

import sys
import stdio
import stddraw
import time
import color
from math import *
import cmath
from picture import Picture
from colorsys import hsv_to_rgb
# from multiprocessing import Pool                

t1 = time.time()
it = 0

ex = float(sys.argv[1])

nx = int(sys.argv[2])
ny = int(sys.argv[3])

t = int(sys.argv[4])

ox = float(sys.argv[5])
oy = float(sys.argv[6])
sx = float(sys.argv[7])
sy = float(sys.argv[8])
splice = 1 #int(sys.argv[9])
splicem = 0 #int(sys.argv[10])
f = sys.argv[9]

zero = 0+0j
def mandelbrot(c, i, j):
	# stdio.write('\r{:02.2f}%'.format(100*float(i)/ny + float(j)/(ny*nx)))
	return check(c, c, maxit, 1)

def check(z, c, i, t):
	global it
	p = abs(z - 1/4)
	if z.real <= p - 2*p**2 + 1/4:
		return 0
	if ex == 2 and (z.real+1)**2 + z.imag**2 < 1/16:
		return 0
	for n in range(i):
		it += 1
		if abs(z) > 2: # escaped
			return t
		else:
			z = z**ex + c
			t += 1
	return 0

"""
def rrow(row, i):
	for j in range(len(row)):
		c = row[j]
		s = min(5*c, 255) #int(256*2*atan(c/10)/pi)
		#stdio.writeln(row)
		#stdio.writeln(s)
		#stdio.write(c)
		#stdio.write(('*' if c == 0 else ' ') + ' ')
		stddraw.setPenColor(color.BLACK if c == 0 else color.Color(s,s/8,0))
		stddraw.rectangle(j, i, 1, 1)

	#stddraw.picture(pic)
	return row
"""
def rrow(row, i):
	stdio.write('\r{:02.2f}%'.format(100*float(i)/nx))
	return [mandelbrot(c, i, j) for j, c in enumerate(row)]

#def calcbrot(spl, splm, a):
#	m = []
#	for i in range(len(a)):
#		#if i % splice == splicem:
#		m.append(rrow([mandelbrot(a[i][j], i, j) for j in range(len(a[i]))], i))
#		#else:
#		#	m.append([-1 for i in range(len(a[i]))])
#	return m
# pool = Pool()
a = [
		[
			complex(sy*(j-float(nx-1)/2)/nx+ox,sx*(-i+float(ny-1)/2)/ny+oy)
			for j in range(0, nx)
		]
		for i in range(0, ny)
	]

stdio.write('...')

m = [rrow(r, i) for i, r in enumerate(a)]
stdio.write('\r{:02.2f}%'.format(100))

t2 = time.time()
t = t2 - t1
tm = int(t/60)
ts = int(t - tm*60)
tms = 1000*(t-ts-tm*60)

stdio.writeln()
stdio.writeln('calc:')
stdio.writeln('{:d}m {:d}s {:.0f}ms'.format(tm, ts, tms))
stdio.writeln(str(it) + ' iterations')


#stddraw.show()
pic = Picture(nx, ny)

for i in range(len(m)):
	#if all(map(lambda c: not c, r)): continue
	stdio.write('\r{:02.2f}%'.format(100*float(i)/ny))
	for j in range(len(m[i])):
		c = m[i][j]
		s = min(c*2, 255) #int(256*2*atan(c/10)/pi)
		#stdio.writeln(s)
		#stdio.write('{:2d}'.format(c))
		#stdio.write(('*' if c == 0 else ' ') + ' ')
		if c == 0:
			pic.set(j, i, color.BLACK)
		elif c == -1:
			pic.set(j, i, color.WHITE)
		else:
			r, g, b = (int(255*i) for i in hsv_to_rgb(
				((sqrt(70*c)) % 100) / 100,
				.5 + .5*cos(1/(c*20*pi)),
				# exp(((c-110)/70)**2)
				exp(c/100-1)/(exp(c/100-1)+19)
				))
			pic.set(j, i, color.Color(r, g, b))
	#stdio.writeln()

stdio.write('\r{:02.2f}%'.format(100))

t3 = time.time()
t = t3 - t2
ts = int(t)
tm = 1000*(t-ts)

stdio.writeln()
stdio.writeln('render:')
stdio.writeln(f'{ts:d}s {tm:.0f}ms')
pic.save(f)
stddraw.setCanvasSize(nx, ny)
stddraw.picture(pic)
stddraw.show()

# python mandelbrot.py 2 400 600 300 .18 -.8 .1 .15 x.png
# python mandelbrot.py 2 1440 2160 1000 .18 -.8 .1 .15 x.png
# python mandelbrot.py 2 400 600 1000 .18 -.8025 .01 .015 x.png
# python mandelbrot.py 2 800 1200 2000 .18237 -.8027 .0004 .0006 x.png
# python mandelbrot.py 2 600 600 1200 .1823 -.8027 .00005 .00005 x.png
# python mandelbrot.py 2 300 300 1600 .18231 -.80268 .00001 .00001 x.png