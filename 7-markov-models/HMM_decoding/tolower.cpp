#include "hmm_prereqs.h"
using namespace std;

int main(int argc, char**argv) {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    setlocale(LC_ALL, ".1251");

    cout << "[ ";
    for (int i = 0; i < 256; i++) {
        cout << "0x" << hex << tolower(i) << ", "; 
    }
    cout << "]" << endl;

    return 0;
}
