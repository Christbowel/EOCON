# minicalc -- fuzzing exercise

A small integer expression evaluator with two bugs that are hard to spot
by reading the code but easy to find with a fuzzer.

## The bugs

**Stack overflow (DoS)**: the recursive descent parser calls itself
without bounding the recursion depth. Each opening parenthesis adds a
frame to the call stack. An input with a few thousand nested parentheses
exhausts the stack and crashes the process. Every function looks correct
on its own; the missing depth check is the kind of thing code review
misses because no single function is wrong.

**Division by zero (SIGFPE)**: the evaluator performs division and modulo
without checking for a zero divisor. An expression like `1/(3-3)` where
the zero comes from a computed sub-expression is not obvious at a glance.

## Build

    make              # builds ./minicalc (normal binary)
    make harness      # builds harness/run (AFL++ instrumented + ASan)

The harness build requires AFL++ (`apt install aflplusplus` on Kali).

## Run

    echo "(4+5)*2" | ./minicalc        # prints 18

## Fuzzing -- dumb (baseline)

    chmod +x scripts/dumb_fuzz.sh
    ./scripts/dumb_fuzz.sh ./minicalc 60

Generates random strings from the calculator character set and feeds
them to minicalc for 60 seconds. Finds very few crashes because random
bytes almost never produce thousands of nested parentheses or the exact
arithmetic that yields a zero divisor.

## Fuzzing -- AFL++ (instrumented)

    make harness
    mkdir -p findings
    afl-fuzz -i corpus -o findings -- ./harness/run

Let it run for a few minutes. AFL++ mutates the corpus seeds, guided by
code coverage, and finds both crash patterns quickly. Crashing inputs
land in `findings/default/crashes/`.

Replay a crash to see the cause:

    ./harness/run < findings/default/crashes/<file>

With ASan enabled the stack overflow produces a clear
`stack-buffer-overflow` or `stack-overflow` diagnostic.

## Why this matters

The bugs emerge from function interactions, not from any single line.
Static review sees correct arithmetic and correct recursion in each
function. A coverage-guided fuzzer explores the input space
systematically and reaches the deep nesting that triggers the crash,
demonstrating why fuzzing complements code review.
