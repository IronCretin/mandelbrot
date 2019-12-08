#include <math.h>
#include <stdio.h>

// compile with:
// cc -fPIC -shared -o libbrot.so mandelbrot.c

double mag2(double x, double y) {
    return x*x + y*y;
}


int check(int maxi, double x0, double y0) {
    double x = x0;
    double y = y0;
    double x1, y1;
    // double p = mag(x - 1/4)
    // if z.real <= p - 2*p**2 + 1/4:
    //     return 0
    // if ex == 2 and (z.real+1)**2 + z.imag**2 < 1/16:
    //     return 0
    for(int i = 0; i < maxi; i++) {
        // printf("%f + %fi\n", x, y);
        if(mag2(x, y) >= 4) { // escaped
            return i;
        } else {
            x1 = x*x - y*y;
            y1 = 2*x*y;
            
            x = x1 + x0;
            y = y1 + y0;
        }
    }
    return -1;
}