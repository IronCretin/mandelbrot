#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// compile with:
// cc -fPIC -shared -o libbrot.so mandelbrot.c

// const int MAXIT = 1000;
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
    int width = atoi(argv[1]);
    int height = atoi(argv[2]);
    float x0 = atof(argv[3]);
    float y0 = atof(argv[4]);
    float xview = atof(argv[5]);
    float yview = atof(argv[6]);
    int MAXIT = atoi(argv[7]);
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
                putchar('@');
            } else {
                printf("\033[1;3%dm", 1 + (steps / 10) % 6);
                // printf("%d", steps % 10);
                // `.',-~^+*:
                switch(steps % 10) {
                    case 0:
                        putchar('`');
                        break;
                    case 1:
                        putchar('.');
                        break;
                    case 2:
                        putchar('-');
                        break;
                    case 3:
                        putchar('\'');
                        break;
                    case 4:
                        putchar(',');
                        break;
                    case 5:
                        putchar(':');
                        break;
                    case 6:
                        putchar('~');
                        break;
                    case 7:
                        putchar('^');
                        break;
                    case 8:
                        putchar('+');
                        break;
                    case 9:
                        putchar('*');
                        break;
                }
                printf("\033[0m");
            }
        }
    putchar('\n');
    }
}