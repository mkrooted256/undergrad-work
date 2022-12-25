#include "hmm_prereqs.h"
#include <vector>
using namespace std;

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    setlocale(LC_ALL, ".1251");

    FILE* f = fopen("1251.full.peter-watts-starfish.txt", "r");
    if(!f) {
        perror("File opening failed");
        return 1;
    }

    map<char, myint> freqs;

    const int checkpoint = 10000;
    unsigned int count = 0, total = 0;
    
    int c; // note: int, not char, required to handle EOF
    bool prev_ws = true;
    while ((c = std::fgetc(f)) != EOF) { // standard C I/O file reading loop
        if (isspace(c)) {
            if (prev_ws) continue; // skip space after space

            c = ' '; // treat all spaces as 0x20
            prev_ws = true;
        }
        prev_ws = false; // not a space!

        // int a = c;
        c = std::tolower(c);
        // if (a!=c && (c-a) != 32) cout << "(" << (char)a << (char)c << ")";

        freqs[c] = freqs[c] + 1;
        ++count;
        if (count == checkpoint) {
            count = 0;
            total += checkpoint;
            cout << "checkpoint: " << total << endl;
        }
    }

    cout << "end" << endl << endl;

    vector<char> valid_chars;

    for (auto i=freqs.begin(); i!=freqs.end(); ++i){
        cout << i->first << " - " << i->second;
        if (notalpha(i->first)) cout << " !!";
        else valid_chars.push_back(i->first);
        cout << endl;
    }

    cout << endl;
    for (auto i=valid_chars.begin(); i!=valid_chars.end(); ++i) {
        cout << *i;
    }
    cout << endl;

    return 0;
}
