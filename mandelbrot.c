#include <math.h>
#include <stdio.h>

// compile with:
// cc -fPIC -shared -o libbrot.so mandelbrot.c

double mag2(double x, double y) {
    return x*x + y*y;
}


int check(int maxi, double x0, double y0) {
    // we have to track the x and y components separately here because c sucks
    // start at zero, after 1 step we hit z so its like starting at z
    double x = 0;
    double y = 0;
    double x1, y1;
    // double x2, y2;
    // double p = mag(x - 1/4)
    // if z.real <= p - 2*p**2 + 1/4:
    //     return 0
    // if ex == 2 and (z.real+1)**2 + z.imag**2 < 1/16:
    //     return 0
    for(int i = 0; i < maxi; i++) {
        // x2 = x*x;
        // y2 = y*y;
        // no need for square root when we can just square the distance
        if(x*x + y*y >= 4) { // escaped
            return i;
        } else {
            // x and y of z^2
            x1 = x*x - y*y;
            y1 = 2*x*y;
            
            // add z0 to z^2
            x = x1 + x0;
            y = y1 + y0;
        }
    }
    // in set
    return -1;
}