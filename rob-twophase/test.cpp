#include <cstdint>
#include <iostream>

int ffs(uint32_t num) {
    if (num == 0) return 0;

    int position = 1;
    while ((num & 1) == 0) {
        num >>= 1;
        position++;
    }

    return position;
}

int ffsll(uint64_t num) {
    if (num == 0) return 0;

    int position = 1;
    while ((num & 1) == 0) {
        num >>= 1;
        position++;
    }

    return position;
}

int main() {
    uint32_t num1 = 24;    // Binary representation: 11000
    uint64_t num2 = 1234;  // Binary representation: 10011010010

    std::cout << "ffs(" << num1 << ") = " << ffs(num1) << std::endl;
    std::cout << "ffsll(" << num2 << ") = " << ffsll(num2) << std::endl;

    return 0;
}