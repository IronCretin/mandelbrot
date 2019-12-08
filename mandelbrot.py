import argparse
import sys
import stdio
import stddraw
import time
import color
from math import *
import cmath
from picture import Picture
from colorsys import hsv_to_rgb


# This bit just sets up the argument handling
parser = argparse.ArgumentParser(description='Generate Mandelbrot set images.')
parser.add_argument('nx', type=int,
                    help='width of image in pixels')
parser.add_argument('ny', type=int,
                    help='height of image in pixels')

parser.add_argument('maxit', type=int,
                    help='maximum number of iterations')

parser.add_argument('centerx', type=float,
                    help='x coordinate of the center of the view')
parser.add_argument('centery', type=float,
                    help='y coordinate of the center of the view')

parser.add_argument('width', type=float,
                    help='width of the view')
parser.add_argument('height', type=float,
                    help='height of the view')

parser.add_argument('--file', '-o', type=str, default=None,
                    help='file to save the image to')
parser.add_argument('--exp', metavar='n', type=float, default=2,
                    help='exponent for the operation (z_i+1 = z_i^n + z_0). Requires --pure')
parser.add_argument('--pure',
                    help='use pure python calculation')



args = parser.parse_args()

# exponent in the process (only works with the python calculator)
ex = args.exp

# size of the display, in pixels
nx = args.nx
ny = args.ny

# maximum number of steps to repeat before giving up for each number
maxit = args.maxit

# region to display
ox = args.centerx
oy = args.centery
sx = args.width
sy = args.height

# dunno what these do
splice = 1 #int(sys.argv[9])
splicem = 0 #int(sys.argv[10])

# file to write to
f = args.file

# for benchmarking
t1 = time.time()

# counts number of iterations (only works for python version)
it = 0

# choose which version of the function to use, python or c
if args.pure:
	# use the pure python version of the function, defined below
	def mandelbrot(z):
		return pycheck(maxit, z)
else:
	# much faster c-based version
	from check import check
	def mandelbrot(z):
		return check(maxit, z.real, z.imag)

def pycheck(i, z):
	"""
	Just take a point called z in the complex plane,
	let z1 be z squared plus z
	and z2 is z1 squared plus z
	and z3 is z2 squared plus z
	and so on, if the series of z's will always stay
	close to z and never trend away
	that point is in the mandelbrot set
	"""
	z0 = z
	global it
	# this chunk here is an optimization to cut out some easy cases
	# that would waste cycles, it checks if the point is in the main
	# bulb of the set
	p = abs(z - 1/4)
	if z.real <= p - 2*p**2 + 1/4:
		return 0
	if ex == 2 and (z.real+1)**2 + z.imag**2 < 1/16:
		return 0

	# up to the max possible iterations for one point
	for t in range(i):
		it += 1
		# once the magnitude goes beyond 2, the point has escaped
		# and is not in the set
		if abs(z) > 2:
			return t
		else:
			# iterate: z_n+1 = z_n^2 + z_0
			z = z**ex + z0
	# if it hasn't escaped after t steps, we assume the point is in the set
	return -1

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
	"""
	this just handles the rows. The commented line below does the progress bar
	"""
	# stdio.write('\r{:02.2f}%'.format(100*float(i)/nx))
	return [mandelbrot(c) for j, c in enumerate(row)]

#def calcbrot(spl, splm, a):
#	m = []
#	for i in range(len(a)):
#		#if i % splice == splicem:
#		m.append(rrow([mandelbrot(a[i][j], i, j) for j in range(len(a[i]))], i))
#		#else:
#		#	m.append([-1 for i in range(len(a[i]))])
#	return m
# pool = Pool()

# this bit generates the grid of numbers, i dont know how the formula
# works and im afraid to touch it
a = [
		[
			complex(sx*(j-float(nx-1)/2)/nx+ox,sy*(-i+float(ny-1)/2)/ny+oy)
			for j in range(0, nx)
		]
		for i in range(0, ny)
	]

stdio.write('...')

# process each row in the gris
m = [rrow(r, i) for i, r in enumerate(a)]
stdio.write('\r{:02.2f}%'.format(100))

# benchmark shit
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

for i, r in enumerate(m):
	# generates the actual image. pizel coordinates are given by position in the array.
	# probably some room for optimization here

	#if all(map(lambda c: not c, r)): continue
	# stdio.write('\r{:02.2f}%'.format(100*float(i)/ny))
	for j, c in enumerate(r):
		s = min(c*2, 255) #int(256*2*atan(c/10)/pi)
		# no idea if it still works, but this is the original text display code
		# from before i'd figured out graphics. I should add a text mode
		#stdio.writeln(s)
		#stdio.write('{:2d}'.format(c))
		#stdio.write(('*' if c == 0 else ' ') + ' ')
		if c == -1: # the point is in the set
			pic.set(j, i, color.BLACK)
		elif c == 0: # outside the circle of radius 2 (maybe not if i changed the algorithm)
			pic.set(j, i, color.BLACK)
		else:
			# this genreates the color based on c, the number of iterations.
			# i just strung math functions together until it spit out a path
			# through hsv space that looked nice
			r, g, b = (int(255*i) for i in hsv_to_rgb(
				((-sqrt(10*c)-90) % 100) / 100,
				.75 + .25*cos(c*pi/20),
				# 1
				exp(c/2-1)/(exp(c/2-1)+10)
				))
			pic.set(j, i, color.Color(r, g, b))
	#stdio.writeln()

stdio.write('\r{:02.2f}%'.format(100))

t3 = time.time()
t = t3 - t2
ts = int(t)
tm = 1000*(t-ts)

# draws the generated image to the canvas (and saves it)
stdio.writeln()
stdio.writeln('render:')
stdio.writeln(f'{ts:d}s {tm:.0f}ms')
if f is not None:
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