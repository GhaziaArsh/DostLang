# DostLang Programming Guide

DostLang is a custom, educational programming language featuring Urdu/Hindi-inspired keywords. It is simple, scope-aware, and supports dynamic type checking, loops, functions, recursion, and arrays.

---

## 1. Program Structure

Every DostLang program must start with `shuru` and end with `khatam`.

```dost
shuru
    # Your program code goes here
khatam
```

## 2. Variables (`rakho`)

Variables are declared using the `rakho` keyword. They must be initialized with an expression value. Subsequent assignments do not require `rakho`.

```dost
rakho age = 22;
rakho height = 5.8;
rakho name = "Ghazia";
rakho isStudent = sach; # sach = True, jhoot = False

age = age + 1; # Re-assignment
```

## 3. Basic I/O

- **Output (`dikhao`)**: Prints values to the console. Accepts one or more comma-separated expressions.
- **Input (`pocho`)**: Pauses program execution to read input from console/UI prompt and stores the result in a variable.

```dost
dikhao("Enter your age below:");
pocho age;
dikhao("You entered age:", age);
```

## 4. Conditionals (`agar` / `warna`)

Allows decision-making based on boolean expressions.

```dost
rakho temp = 35;

agar temp > 40 {
    dikhao("Garmi buhat hai!");
} warna {
    agar temp < 20 {
        dikhao("Sardi hai!");
    } warna {
        dikhao("Khushgawar mausam!");
    }
}
```

## 5. Loops (`jabtak`)

While loops execute statements in a block as long as the condition remains true.

```dost
rakho count = 1;
jabtak count <= 5 {
    dikhao("Counting:", count);
    count = count + 1;
}
```

## 6. Functions (`kaam` & `wapas`)

Define reusable logic blocks using `kaam`. Use `wapas` to return values.

```dost
kaam square(n) {
    wapas n * n;
}

rakho res = square(5);
dikhao("Square of 5 is:", res);
```

### Recursion
Functions can call themselves recursively:

```dost
kaam fib(n) {
    agar n <= 1 {
        wapas n;
    } warna {
        wapas fib(n - 1) + fib(n - 2);
    }
}

dikhao("10th Fibonacci number is:", fib(10));
```

## 7. Arrays

Create lists of variables using square brackets. Access and modify elements via zero-based indices.

```dost
rakho fruits = ["apple", "banana", "mango"];
dikhao("First fruit:", fruits[0]);

fruits[1] = "peach";
dikhao("Updated fruits:", fruits);
```
