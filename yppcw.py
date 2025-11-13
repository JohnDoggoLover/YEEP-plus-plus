#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
import platform

if len(sys.argv) < 2:
    print("Usage: python yppc.py <sourcefile>")
    sys.exit(1)

srcpath = sys.argv[1]

# Read input file (whatever is inside)
with open(srcpath, "r", encoding="utf-8") as fh:
    fcont = fh.read()

# output base name (foo.txt -> foo)
t1 = os.path.splitext(os.path.basename(srcpath))[0]
out_py = t1 + ".py"

# Template for the full interpreter. Use a unique marker {CODE_MARKER} that we'll replace
content_template = r"""
import sys


KEYWORDS = ["var", "print", "call", "jmp", "ret", "nop", "add", "sub", "mul", "div", "inp","cmp","gj","lj","ej"]
def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def tokenizer(s: str):
    lines = s.split("\n")
    tokens = []
    for line in lines:
        tokens.extend(subtok(line))
    return tokens


def subtok(s: str) -> list[str]:
    parts = []
    current = []
    in_quotes = False

    i = 0
    while i < len(s):
        c = s[i]

        if c == '"':
            in_quotes = not in_quotes
            current.append(c)
        elif c == ' ' and not in_quotes:
            if current:
                parts.append(''.join(current))
                current = []
        else:
            current.append(c)
        i += 1

    if current:
        parts.append(''.join(current))

    return parts


def identall(tokens):
    i = 0
    arry = []
    while i < len(tokens):
        arry.append(identify(tokens[i]))
        i = i + 1
    return arry  


def identify(token):
    if token[-1] == ":":
        return ("Label", token[:-1])
    if token[0] == '"' and token[-1] == '"':
        return ("String", token[1:-1])  # strip quotes here
    elif is_number(token):
        return ("Number", token)
    elif token in KEYWORDS:
        return ("Keyword", token)
    elif token == "EOF":
        return ("EOF", None)
    else:
        return ("Identifier", token)



def ParseStart(code):
        return identall(tokenizer(code))

def lexer(lexcode):
    gt = lt = eq = False
    vars = {}
    labels = {}
    retpos = 0

    # --- Pass 1: collect labels ---
    for idx, (title, val) in enumerate(lexcode):
        if title == "Label":
            labels[val] = idx

    # --- Pass 2: execute ---
    i = 0
    while i < len(lexcode):
        title, val = lexcode[i]

        # ----------------------------
        # Handle Keywords / Instructions
        # ----------------------------
        if title == "Keyword":

            # --- no operation ---
            if val == "nop":
                pass

            # --- print ---
            elif val == "print" and i + 1 < len(lexcode):
                next_title, next_val = lexcode[i + 1]
                if next_title == "String":
                    print(next_val)
                elif next_title == "Identifier":
                    print(vars.get(next_val, f"Undefined variable: {next_val}"))
                else:
                    print("Syntax error: 'print' expects a string or variable")
                i += 1

            # --- cmp ---
            elif val == "cmp" and i + 2 < len(lexcode):
                nt, nv = lexcode[i + 1]
                nnt, nnv = lexcode[i + 2]

                left = float(vars[nv]) if nt == "Identifier" else float(nv)
                right = float(vars[nnv]) if nnt == "Identifier" else float(nnv)

                gt, lt, eq = left > right, left < right, left == right
                i += 2

            # --- var assignment ---
            elif val == "var" and i + 2 < len(lexcode):
                name_title, name_val = lexcode[i + 1]
                value_title, value_val = lexcode[i + 2]

                if name_title != "Identifier":
                    print("Syntax error: expected variable name after 'var'")
                else:
                    if value_title == "String":
                        vars[name_val] = value_val
                    elif value_title == "Number":
                        vars[name_val] = float(value_val)
                    elif value_title == "Identifier":
                        vars[name_val] = vars.get(value_val, 0)
                    else:
                        print(f"Syntax error: unexpected token '{value_val}'")
                i += 2

            # --- arithmetic operations ---
            elif val in ("add", "sub", "mul", "div") and i + 2 < len(lexcode):
                name_title, name_val = lexcode[i + 1]
                value_title, value_val = lexcode[i + 2]

                if name_title != "Identifier":
                    print(f"Syntax error: expected variable name after '{val}'")
                else:
                    a = float(vars.get(name_val, 0))
                    b = float(vars.get(value_val, 0)) if value_title == "Identifier" else float(value_val)

                    if val == "add":
                        vars[name_val] = a + b
                    elif val == "sub":
                        vars[name_val] = a - b
                    elif val == "mul":
                        vars[name_val] = a * b
                    elif val == "div":
                        vars[name_val] = a / b
                i += 2

            # --- input ---
            elif val == "inp" and i + 2 < len(lexcode):
                next_title, next_val = lexcode[i + 1]
                nnext_title, nnext_val = lexcode[i + 2]
                if next_title == "Identifier":
                    if nnext_title == "Number" and float(nnext_val) < 1:
                        vars[next_val] = input()
                    else:
                        vars[next_val] = float(input())
                else:
                    print("Syntax error: expected variable name for input")
                    quit()
                i += 2

            # --- call ---
            elif val == "call" and i + 1 < len(lexcode):
                next_title, next_val = lexcode[i + 1]
                retpos = i + 2
                if next_title == "String":
                    i = labels[next_val]
                elif next_title == "Identifier":
                    i = labels.get(vars.get(next_val, ""), i)
                else:
                    print("Syntax error: 'call' expects a label name")
                    break
                continue  # skip i += 1

            # --- unconditional jump ---
            elif val == "jmp" and i + 1 < len(lexcode):
                next_title, next_val = lexcode[i + 1]
                if next_title == "String":
                    i = labels[next_val]
                elif next_title == "Identifier":
                    i = labels.get(vars.get(next_val, ""), i)
                else:
                    print("Syntax error: 'jmp' expects a label name")
                    break
                continue  # skip i += 1

            # --- return ---
            elif val == "ret":
                i = retpos
                continue

            # --- conditional jumps ---
            elif val == "gj" and i + 1 < len(lexcode) and gt:
                next_title, next_val = lexcode[i + 1]
                if next_title == "String":
                    i = labels[next_val]
                elif next_title == "Identifier":
                    i = labels.get(vars.get(next_val, ""), i)
                continue

            elif val == "lj" and i + 1 < len(lexcode) and lt:
                next_title, next_val = lexcode[i + 1]
                if next_title == "String":
                    i = labels[next_val]
                elif next_title == "Identifier":
                    i = labels.get(vars.get(next_val, ""), i)
                continue

            elif val == "ej" and i + 1 < len(lexcode) and eq:
                next_title, next_val = lexcode[i + 1]
                if next_title == "String":
                    i = labels[next_val]
                elif next_title == "Identifier":
                    i = labels.get(vars.get(next_val, ""), i)
                continue
        # ----------------------------
        # Handle EOF
        # ----------------------------
        elif title == "EOF":
            break

        i += 1  # increment i if no jump/continue

# ----------------------------
# Main entry
# ----------------------------
if __name__ == "__main__":
    code = {CODE_MARKER}
    lexer(ParseStart(code))
"""

# Replace the marker with repr(fcont) so contents are safely embedded as a Python literal
content = content_template.replace("{CODE_MARKER}", repr(fcont))

# Write the full generated interpreter .py
with open(out_py, "w", encoding="utf-8") as fh:
    fh.write(content)

print(f"Wrote generated interpreter to: {out_py}")

# Build with PyInstaller
print("Building with PyInstaller (this may take a moment)...")
subprocess.run(["pyinstaller", "--onefile", out_py], check=True)

# Determine source executable location depending on platform
system = platform.system()
built_name = t1 + ".exe"
#thanks a lot python....
dist_src = os.path.join("dist", built_name)
if not os.path.exists(dist_src):
    print("ERROR: built file not found at", dist_src)
    sys.exit(1)

# Copy built executable into current working directory
dst = os.path.join(os.getcwd(), os.path.basename(dist_src))
shutil.copy(dist_src, dst)
print("Copied built executable to:", dst)

# Cleanup build artifacts
for thing in ("build", "dist", out_py, t1 + ".spec", "__pycache__"):
    if os.path.isdir(thing):
        shutil.rmtree(thing, ignore_errors=True)
    elif os.path.exists(thing):
        try:
            os.remove(thing)
        except Exception:
            pass

print("Done.")
