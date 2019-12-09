#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// compile with:
// cc -fPIC -shared -o libbrot.so mandelbrot.c

const int MAXIT = 100;
// const int SIZE = 30;

int check(int maxit, double x0, double y0) {
    double x1, y1, x, y;
    // we have to track the x and y components separately here because c sucks
    // start at zero, after 1 step we hit z so its like starting at z
    x = 0;
    y = 0;
    for(int i = 0; i < maxit; i++) {
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

int main(int argc, char *argv[]) {
    int SIZE = atoi(argv[1]);
    int steps;
    float x, y;
    // int cells[30][30];
    printf("\033[0;31m"); 
    for(int i = 0; i < SIZE/2; i++) {
        y = 4.0 / (SIZE/2) * -i + 2;
        for(int j = 0; j < SIZE; j++) {
            x = 4.0 / (SIZE - 1) * j - 2;
            // printf("%.2f + %.2fi", x, y);
            steps = check(MAXIT, x, y);
            if(steps == -1) {
                printf("*");
            } else {
                printf(" ");
            }
        }
    printf("\n");
    }
}