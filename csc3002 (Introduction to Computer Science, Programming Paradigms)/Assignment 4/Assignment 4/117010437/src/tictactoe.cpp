#include "tictactoe.h"

using namespace std;

class TicTacToe {           //class
public:
    int switch = 0;         //switch variable
    int x,y = 0;            // x,y
    char format = '*';
    char tic[3][3];
    void start();           //start
    void TTT();             //output
    int check();            //check
    TicTacToe() {};
};

void TicTacToe::TTT(){
    for (int i = 0; i <3; i++) {
        for (int j = 0; j < 3; j++) {
        }
    }
}

int TicTacToe::check() {
    int hor_R = 0;
    int hor_B = 0;
    int ver_R = 0;
    int ver_B = 0;
    int R_diagonal_R = 0;
    int R_diagonal_B = 0;
    int L_diagonal_R = 0;
    int L_diagonal_B = 0;

    for (int i =0; i<3; i++) {
        hor_R = 0;
        hor_B = 0;
        ver_R = 0;
        ver_B = 0;
        for (int j =0; j< 3; j++) {
            if (tic[i][j] == 'O') {
                hor_R++;
            }
            else if (tic[i][j] == 'X') {
                hor_B++;
            }
            if (tic[j][i] == 'O') {
                ver_R++;
            }
            else if (tic[j][i] == 'X') {
                ver_B++;
            }
            if (i == j && tic[i][j] == 'O') {
                L_diagonal_R++;
            }
            else if (i == j && tic[i][j] == 'X') {
                L_diagonal_B++;
            }
            if ((i+j) == 2 && tic[i][j] == 'O') {
                R_diagonal_R++;
            }
            else if ((i+j) == 2 && tic[i][j] == 'X') {
                R_diagonal_B++;
            }
        }
        if (hor_R == 3 || hor_B == 3 || ver_R == 3 || ver_B == 3 || L_diagonal_R == 3 || L_diagonal_B == 3 || R_diagonal_R == 3 || R_diagonal_B || 3) {
            switch = 3;
            break;
        }

    }
    return switch;
}

void TicTacToe::start()
{
    cout << "TicTacToe start";
    for (int i = 0; i < 3; i++) {
        cout << endl;
        for (int j =0; j < 3; j++) {
            tic[i][j] = '*';
        }
    }
    cout << endl;
    while (switch != 3) {
        cout << " Enter X : ";
        cin >> x;
        cout << " Enter Y : ";
        cin >> y;
        cout << " Enter O or X : ";
        cin >> format;
        tic[x][y] = format;
        TTT()
        cin.ignore();
        switch = check();
    }
    cout << switch;
    cout << "TicTacToe over";
}
int main() {
    TicTacToe gm;
    gm.start();
    return 0;
}
