// Example program
#include <iostream>
#include <string>

using namespace std;

int main()
{
    int8_t a, b;
    int ax, bx;
    cout << "a: ";
    cin >> ax;
    cout << "b: ";
    cin >> bx;
    
    a = ax; b = bx;
    const int8_t stop  = a - b;
    for (int8_t i = a; i > stop; i--) {
        cout << (int) i << endl;
    }
}
