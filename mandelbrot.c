#include <math.h>
#include <stdio.h>

// compile with:
// cc -fPIC -shared -o libbrot.so mandelbrot.c

double mag2(double x, double y) {
    return x*x + y*y;
}


void check(int maxit, double xs[], double ys[], int size, int out[]) {
    int escaped;
    double x0, y0, x1, y1, x, y;
    for(int n = 0; n < size; n++) {
        escaped = 0;
        x0 = xs[n];
        y0 = ys[n];
        // we have to track the x and y components separately here because c sucks
        // start at zero, after 1 step we hit z so its like starting at z
        x = 0;
        y = 0;
        for(int i = 0; i < maxit; i++) {
            // x2 = x*x;
            // y2 = y*y;
            // no need for square root when we can just square the distance
            if(x*x + y*y >= 4) { // escaped
                escaped = 1;
                out[n] = i;
                break;
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
        if (!escaped){
            out[n] = -1;
        }
    }
}