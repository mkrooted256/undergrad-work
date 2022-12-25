#include "hmm_prereqs.h"
using namespace std;

int main(int argc, char**argv) {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    setlocale(LC_ALL, ".1251");

    FILE* f = fopen(argv[1], "r");
    if(!f) {
        perror("File opening failed");
        return 1;
    }

    trans_data data;
    data.populate();

    const int checkpoint = 10000;
    unsigned int count = 0, total = 0, true_total = 0;

    int prev_c = 0x20;
    int c; // note: int, not char, required to handle EOF
    bool prev_ws = true;
    while ((c = std::fgetc(f)) != EOF) { // standard C I/O file reading loop
        ++true_total;
        if (notalpha(c)) {
            // cout << "notalpha ";
            c = 0x20;
        }
        if (c == 0x20) {
            // cout << "space ";
            if (prev_ws) {
                // cout << "skip" << endl;
                continue; // skip space after space
            }
            // cout << "set-prevws ";
            prev_ws = true;
        } else {   
            // cout << "unset-prevws ";
            prev_ws = false; // not a space!
        }
        // int a = c;
        c = std::tolower(c);
        // if (a!=c && (c-a) != 32) cout << "(" << (char)a << (char)c << ")";

        // cout << "transition " << prev_c << ">" << c << endl;
        data.record_transition(prev_c, c);
        prev_c = c;

        ++count;
        if (count == checkpoint) {
            count = 0;
            total += checkpoint;
            cout << "checkpoint: " << total << endl;
        }
    }

    cout << "end" << endl << endl << endl;

    data.print();

    FILE* ofdata = fopen("transitions.dat", "wb");
    fwrite(&data, sizeof(data), 1, ofdata);

    return 0;
}
