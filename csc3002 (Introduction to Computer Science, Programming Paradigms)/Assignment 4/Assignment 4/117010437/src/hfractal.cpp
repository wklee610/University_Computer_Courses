#include "hfractal.h"
using namespace std;

void drawHFractal(GWindow & gw, double x, double y, double size, int order) {
    if (order == 0) {
    gw.drawLine(x+(size/2),y,x-(size/2),y);
    gw.drawLine(x+(size/2),y+(size/2),x+(size/2),y-(size/2));
    gw.drawLine(x-(size/2),y+(size/2),x-(size/2),y-(size/2));
}

    if (order != 0) {
    drawHFractal(gw,x,y,size,order-1);
    drawHFractal(gw,x+(size/2),y+(size/2),size/2,order-1);
    drawHFractal(gw,x+(size/2),y-(size/2),size/2,order-1);
    drawHFractal(gw,x-(size/2),y-(size/2),size/2,order-1);
    drawHFractal(gw,x-(size/2),y+(size/2),size/2,order-1);
}
\

PROVIDED_TEST("hfractal", HFRACTAL) {
    GWindow gw;
    double xc = gw.getWidth() / 2;
    double yc = gw.getHeight() / 2;
    drawHFractal(gw, xc, yc, 100, 3);
}
