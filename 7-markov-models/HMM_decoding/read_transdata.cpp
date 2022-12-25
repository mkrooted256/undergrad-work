#include <cstdio>
#include <iostream>
#include <fstream>
#include <map>
#include <Windows.h>
#include <locale>
#include <cstring>
#include <algorithm>
#include <iomanip>
using namespace std;


struct trans_data {
    char characters[35];
    unsigned long matrix[35*35] = {0};
    unsigned long charcounts[35] = {0};

    void populate() {
        strncpy(characters, "іґєїабвгдежзийклмнопрстуфхцчшщьюя '", 35);
        sort(characters, characters+35);
        for (auto i=characters+1; i!=characters+35; i++) {
            if (*i < *(i-1)) cout << "data::populate() : ACHTUNG! sorting failed at " << *(i-1) << ", " << *(i) <<" (" << i-characters << ")" << endl; 
        }
    }

    void record_transition(char from, char to) {
        char* ix = lower_bound(characters, characters+35, from);
        char* jx = lower_bound(characters, characters+35, to);
        if (*ix != from || *jx != to) {
            cout << "  invalid characters " << from << " or " << to << endl;
            return;
        }
        int i = ix - characters;
        int j = jx - characters;
        ++matrix[i*35 + j];
        ++charcounts[i];
    }

    void print() {
        const int padding = 20;
        cout << "  ";
        for (int i = 0; i<35; i++) {
            cout << setw(padding) << characters[i];
        }
        cout << endl;
        for (int i=0; i<35; i++) {
            auto rowstart = matrix + 35*i;
            cout << characters[i] << " ";
            for (int j=0; j<35; j++) {
                cout << setw(padding) << fixed << setprecision(5) << double(*(rowstart+j)) / charcounts[i];
            }
            cout << endl;
        }
    }
};

int main(int argc, char ** argv) {
    ifstream in(argv[1], ios_base::in | ios_base::binary);
    trans_data data;
    in.read((char*)&data, sizeof(data));
    data.print();
    return 0;
}
