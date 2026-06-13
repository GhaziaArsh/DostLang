# dostlang 🌟

> **A toy programming language written in Python — with Urdu-inspired keywords!**

Made by **Ghazia, Javeria, and Iqra**



## What is DostLang?

DostLang is a dynamically typed, interpreted toy programming language built in Python. It uses Urdu/Pakistani-inspired keywords, making it fun and approachable for Urdu speakers while teaching core programming concepts like variables, loops, conditionals, functions, and recursion.



## Quick Start

```
shuru
    dikhao("Assalam-o-Alaikum, DostLang!");
khatam
```

---

## Keywords

| Keyword   | Meaning           |
|-----------|-------------------|
| `shuru`   | Start (entry point) |
| `khatam`  | End (exit point)  |
| `rakho`   | Declare variable  |
| `dikhao`  | Print to console  |
| `agar`    | If                |
| `warna`   | Else / Else-if    |
| `jabtak`  | While loop        |
| `kaam`    | Function          |
| `wapas`   | Return            |
| `sach`    | True              |
| `jhoot`   | False             |

---

## Language Features

### Program Structure
Every program must start with `shuru` and end with `khatam`. Anything outside is ignored.

```
shuru
    # your code here
khatam
```

---

### Variables
Declare with `rakho`. DostLang is dynamically typed.

```
shuru
    rakho a = 10;
    rakho b = "hello";
    rakho c = sach;
    a = a + 1;
khatam
```

---

### Data Types

- **Numbers** — `10`, `3.14`, `-5`
- **Strings** — `"hello"` or `'hello'`
- **Booleans** — `sach` (true), `jhoot` (false)

---

### Print Output

```
shuru
    dikhao("Hello!");
    dikhao(1, 2, "three", sach);
khatam
```

---

### Conditionals

```
shuru
    rakho a = 10;
    agar (a < 20) {
        dikhao("less than 20");
    } warna {
        agar (a < 25) {
            dikhao("less than 25");
        } warna {
            dikhao("25 or more");
        }
    }
khatam
```

---

### Loops

```
shuru
    rakho i = 0;
    jabtak (i < 5) {
        i = i + 1;
        dikhao(i);
    }
khatam
```

---

### Functions & Recursion

```
shuru
    kaam factorial(n) {
        agar (n <= 1) {
            wapas 1;
        } warna {
            wapas n * factorial(n - 1);
        }
    }
    dikhao(factorial(5));  # Output: 120
khatam
```

---

## Code Templates

The DostLang Playground includes these built-in templates:

| Template | Description |
|----------|-------------|
| Hello World | Print a greeting |
| Variables (Rakho) | Declare and update values |
| Arithmetic Operations | Math expressions |
| Decision Making (Agar/Warna) | Conditional flows |
| Looping (Jabtak) | While loop examples |
| Functions (Kaam) | Function declaration and calls |
| Recursion (Factorial) | Recursive function example |
| Array Operations | Basic array usage |

---

## Rules Summary

- Every program **must** start with `shuru` and end with `khatam`
- Every statement ends with a **semicolon** `;`
- Comments start with `#`
- Variables must be declared with `rakho` before use
- Code blocks use curly braces `{ }`
- Conditions must be wrapped in parentheses `( )`
- Booleans are `sach` and `jhoot` — not `true`/`false`

---

## Project Structure

```
dostlang/
├── lexer.py        # Tokenizer / Lexer
├── parser.py       # Parser (AST builder)
├── interpreter.py  # Tree-walk interpreter
├── main.py         # Entry point
└── README.md       # This file
```

---

## Made with ❤️ by

**Ghazia, Javeria, and Iqra**
