#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "../src/minicalc.h"

__AFL_FUZZ_INIT();

int main(void)
{
    __AFL_INIT();

    unsigned char *buf = __AFL_FUZZ_TESTCASE_BUF;

    while (__AFL_LOOP(10000)) {
        int len = __AFL_FUZZ_TESTCASE_LEN;
        if (len < 1 || len > 524000)
            continue;

        static char input[524001];
        memcpy(input, buf, len);
        input[len] = '\0';

        token_list tl;
        if (tokenize(input, &tl) != 0)
            continue;

        evaluate(&tl);
    }

    return 0;
}
