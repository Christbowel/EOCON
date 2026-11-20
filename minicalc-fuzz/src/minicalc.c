#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "minicalc.h"

static long parse_expr(token_list *tl);
static long parse_term(token_list *tl);
static long parse_factor(token_list *tl);

static token peek(token_list *tl)
{
    return tl->items[tl->pos];
}

static token advance(token_list *tl)
{
    return tl->items[tl->pos++];
}

int tokenize(const char *line, token_list *tl)
{
    int i = 0;
    tl->count = 0;
    tl->pos = 0;

    while (line[i] != '\0' && line[i] != '\n') {
        if (isspace(line[i])) {
            i++;
            continue;
        }

        if (tl->count >= MAX_TOKENS - 1)
            return -1;

        if (isdigit(line[i])) {
            long val = 0;
            while (isdigit(line[i])) {
                val = val * 10 + (line[i] - '0');
                i++;
            }
            tl->items[tl->count].type = TOK_NUM;
            tl->items[tl->count].value = val;
            tl->count++;
            continue;
        }

        token_type tt;
        switch (line[i]) {
        case '+': tt = TOK_PLUS;    break;
        case '-': tt = TOK_MINUS;   break;
        case '*': tt = TOK_STAR;    break;
        case '/': tt = TOK_SLASH;   break;
        case '%': tt = TOK_PERCENT; break;
        case '(': tt = TOK_LPAREN;  break;
        case ')': tt = TOK_RPAREN;  break;
        default:
            return -1;
        }

        tl->items[tl->count].type = tt;
        tl->items[tl->count].value = 0;
        tl->count++;
        i++;
    }

    tl->items[tl->count].type = TOK_END;
    tl->items[tl->count].value = 0;
    tl->count++;
    return 0;
}

static long parse_factor(token_list *tl)
{
    token t = peek(tl);

    if (t.type == TOK_NUM) {
        advance(tl);
        return t.value;
    }

    if (t.type == TOK_LPAREN) {
        advance(tl);
        long val = parse_expr(tl);
        if (peek(tl).type == TOK_RPAREN)
            advance(tl);
        return val;
    }

    if (t.type == TOK_MINUS) {
        advance(tl);
        return -parse_factor(tl);
    }

    return 0;
}

static long parse_term(token_list *tl)
{
    long left = parse_factor(tl);

    while (peek(tl).type == TOK_STAR ||
           peek(tl).type == TOK_SLASH ||
           peek(tl).type == TOK_PERCENT) {
        token op = advance(tl);
        long right = parse_factor(tl);
        if (op.type == TOK_STAR)
            left = left * right;
        else if (op.type == TOK_SLASH)
            left = left / right;
        else
            left = left % right;
    }

    return left;
}

static long parse_expr(token_list *tl)
{
    long left = parse_term(tl);

    while (peek(tl).type == TOK_PLUS ||
           peek(tl).type == TOK_MINUS) {
        token op = advance(tl);
        long right = parse_term(tl);
        if (op.type == TOK_PLUS)
            left = left + right;
        else
            left = left - right;
    }

    return left;
}

long evaluate(token_list *tl)
{
    tl->pos = 0;
    return parse_expr(tl);
}

#ifndef HARNESS_MODE
int main(void)
{
    static char line[524288];

    while (fgets(line, sizeof(line), stdin)) {
        static token_list tl;
        if (tokenize(line, &tl) != 0) {
            fprintf(stderr, "syntax error\n");
            continue;
        }
        printf("%ld\n", evaluate(&tl));
    }

    return 0;
}
#endif
