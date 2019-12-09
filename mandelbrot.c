#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// compile with:
// cc -fPIC -shared -o libbrot.so mandelbrot.c

const int MAXIT = 1000;
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
    int height = atoi(argv[2]);
    int width = atoi(argv[1]);
    float x0 = -.5;
    float y0 = 0;
    float xview = 3;
    float yview = 2;
    int steps;
    float x, y;
    // int cells[30][30];
    for(int i = 0; i < height; i++) {
        y = yview / (height - 1) * -i - y0 + yview/2;
        for(int j = 0; j < width; j++) {
            x = xview / (width - 1) * j + x0 - xview/2;
            // printf("%.2f + %.2fi", x, y);
            steps = check(MAXIT, x, y);
            if(steps == -1) {
                printf("*");
            } else {
                printf("\033[0;3%dm", 1 + (steps / 10) % 6);
                printf("%d", steps % 10);
                // switch(steps/6) {
                //     case 1:
                //     printf(" ");
                //     break;
                //     case 2:
                //     printf("`");
                //     break;
                //     default:
                //     printf(".");
                // }
                printf("\033[0m");
            }
        }
    printf("\n");
    }
}