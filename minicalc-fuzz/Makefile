CC      = cc
AFL_CC  = afl-clang-fast
CFLAGS  = -std=c99 -Wall -Wextra -g
AFLFLAGS = -std=c99 -Wall -Wextra -g -fsanitize=address

.PHONY: all clean harness

all: minicalc

minicalc: src/minicalc.c src/minicalc.h
	$(CC) $(CFLAGS) -o $@ src/minicalc.c

harness: harness/run

harness/run: harness/minicalc_harness.c src/minicalc.c src/minicalc.h
	$(AFL_CC) $(AFLFLAGS) -DHARNESS_MODE -o $@ harness/minicalc_harness.c src/minicalc.c

clean:
	rm -f minicalc harness/run
