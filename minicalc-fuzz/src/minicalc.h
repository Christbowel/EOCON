#ifndef MINICALC_H
#define MINICALC_H

#define MAX_TOKENS 131072

typedef enum {
    TOK_NUM,
    TOK_PLUS,
    TOK_MINUS,
    TOK_STAR,
    TOK_SLASH,
    TOK_PERCENT,
    TOK_LPAREN,
    TOK_RPAREN,
    TOK_END
} token_type;

typedef struct {
    token_type type;
    long value;
} token;

typedef struct {
    token items[MAX_TOKENS];
    int count;
    int pos;
} token_list;

int tokenize(const char *line, token_list *tl);
long evaluate(token_list *tl);

#endif
