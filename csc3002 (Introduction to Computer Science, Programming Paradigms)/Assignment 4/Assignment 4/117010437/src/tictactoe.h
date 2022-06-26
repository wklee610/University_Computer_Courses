#ifndef TICTACTOE_H
#define TICTACTOE_H
#include <grid.h>
#include <gwindow.h>
#include "testing/SimpleTest.h"
enum Player {
    COMPUTER,
    USER,
    NONE
};

class TicTacToe
{
    Grid<Player> grid;
public:
    TicTacToe();
};

void start_game();


#endif // TICTACTOE_H
