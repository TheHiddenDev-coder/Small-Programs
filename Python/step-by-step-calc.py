import re
import sys

NUMBER_RE = re.compile(r'^\d+(\.\d+)?')

def format_num(n):
    # Convert number to string; remove unnecessary .0
    try:
        val = float(n)
    except:
        return str(n)
    return str(int(val)) if val.is_integer() else str(val)

def tokenize(expr):
    expr = expr.strip()
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c in '()+-*/^':
            # Unary minus
            if c == '-' and (not tokens or tokens[-1] in ('(', '+', '-', '*', '/', '^')):
                if i + 1 < len(expr) and expr[i+1] == '(':
                    tokens.extend(['0', '-'])
                    i += 1
                    continue
                # Unary minus before number
                j = i + 1
                m = re.match(r'\d+(\.\d+)?', expr[j:])
                if m:
                    tokens.append('-' + m.group(0))
                    i = j + len(m.group(0))
                    continue
                tokens.append('-')
                i += 1
                continue
            # Unary plus
            if c == '+' and (not tokens or tokens[-1] in ('(', '+', '-', '*', '/', '^')):
                i += 1
                continue
            tokens.append(c)
            i += 1
            continue
        # Number
        m = re.match(r'\d+(\.\d+)?', expr[i:])
        if m:
            tokens.append(m.group(0))
            i += len(m.group(0))
            continue
        print("Invalid character:", c)
        sys.exit(1)
    return tokens

def find_matching_paren(tokens, start):
    depth = 0
    for i in range(start, len(tokens)):
        if tokens[i] == '(':
            depth += 1
        elif tokens[i] == ')':
            depth -= 1
            if depth == 0:
                return i
    return -1

def compute_one_operation(tokens):
    # Operator precedence: ^ > * / > + -
    op_idx = None
    # Right-associative '^'
    for i in range(len(tokens)-1, -1, -1):
        if tokens[i] == '^':
            op_idx = i
            break
    if op_idx is None:
        for i, t in enumerate(tokens):
            if t in ('*', '/'):
                op_idx = i
                break
    if op_idx is None:
        for i, t in enumerate(tokens):
            if t in ('+', '-'):
                op_idx = i
                break
    if op_idx is None:
        return tokens
    left = float(tokens[op_idx-1])
    right = float(tokens[op_idx+1])
    op = tokens[op_idx]
    if op == '+':
        res = left + right
    elif op == '-':
        res = left - right
    elif op == '*':
        res = left * right
    elif op == '/':
        res = left / right
    elif op == '^':
        res = pow(left, right)
    else:
        print("Unknown operator:", op)
        sys.exit(1)
    return tokens[:op_idx-1] + [format_num(res)] + tokens[op_idx+2:]

def evaluate_tokens(tokens, print_steps=True):
    while '(' in tokens:
        last_open = None
        for i, t in enumerate(tokens):
            if t == '(':
                last_open = i
        close = find_matching_paren(tokens, last_open)
        if close == -1:
            print("Error: mismatched parentheses")
            sys.exit(1)
        sub = tokens[last_open+1:close]
        while len(sub) > 1:
            sub = compute_one_operation(sub)
        tokens = tokens[:last_open] + [sub[0]] + tokens[close+1:]
        if print_steps:
            print("=" + ''.join(tokens) + "=" if len(tokens) > 1 else format_num(tokens[0]))
    while len(tokens) > 1:
        tokens = compute_one_operation(tokens)
        if print_steps:
            print("=" + ''.join(tokens) + "=" if len(tokens) > 1 else format_num(tokens[0]))
    return tokens[0]

def main():
    while True:
        try:
            expr = input("Enter expression (or 'no' to quit): ").strip()
        except EOFError:
            break
        if not expr:
            print("No expression entered.")
            continue
        if expr.lower() == "no":
            print("Exiting...")
            break
        tokens = tokenize(expr)
        print(''.join(tokens) + "=")
        result = evaluate_tokens(tokens, print_steps=True)
        print(format_num(result))

if __name__ == "__main__":
    main()
