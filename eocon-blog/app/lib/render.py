def eval_expr(code):
    return str(eval(code))


def render(body):
    text = str(body)
    while "{{" in text and "}}" in text[text.index("{{"):]:
        i = text.index("{{")
        j = text.index("}}", i)
        expr = text[i + 2:j].strip()
        try:
            result = eval_expr(expr)
        except Exception as e:
            result = "{{error: " + str(e) + "}}"
        text = text[:i] + result + text[j + 2:]
    return text
