
dostlang
A Toy Programming Language Written in Python
Complete Language Reference & Rules Documentation
Made by Ghazia, Javeria, and Iqra
1. Overview
DostLang is a dynamically typed, interpreted toy programming language implemented in Python. It uses Urdu/Pakistani-inspired keywords, making it approachable and fun for Urdu speakers while teaching fundamental programming concepts.

2. Keywords Reference
All reserved keywords in DostLang and their English equivalents:

Keyword	Meaning	Usage
shuru	Start / Begin	Program entry point
khatam	End / Finish	Program terminator
rakho	Keep / Declare	Variable declaration
dikhao	Show / Display	Print to console
agar	If	Conditional block
warna	Otherwise / Else	Else / Else-if block
jabtak	While / As long as	Loop construct
kaam	Work / Function	Function declaration
wapas	Return / Give back	Return from function
sach	True	Boolean true value
jhoot	False	Boolean false value

3. Program Structure
3.1 Entry Point & Exit Point
Every DostLang program must begin with the keyword shuru and end with khatam. Any code written outside these boundaries is completely ignored by the interpreter.

shuru	Marks the beginning of the program. Acts as the entry point.

khatam	Marks the end of the program. Everything after this is ignored.

Basic Program Template
# Anything here is IGNORED

shuru
    # Your code goes here
    dikhao("Assalam-o-Alaikum, DostLang!");
khatam

# Anything here is also IGNORED

3.2 Program Rules
•	Every program MUST start with shuru
•	Every program MUST end with khatam
•	Code outside shuru...khatam is silently ignored
•	Statements inside shuru...khatam are executed sequentially
•	Each statement ends with a semicolon (;)
•	Comments begin with # and extend to the end of the line
•	Indentation is optional but recommended for readability
•	Curly braces { } define code blocks (conditionals, loops, functions)

4. Data Types
DostLang is dynamically typed — you do not declare types explicitly. The interpreter determines the type at runtime.

Type	Description	Examples
Number	Integer or floating-point numeric values	10, 3.14, -5, 100
String	Text enclosed in double or single quotes	"hello", 'world'
Boolean	Logical truth values (Urdu-named)	sach (true), jhoot (false)
Expression	Computed value from arithmetic/logic	10 + (15 * 20)

Type Examples
shuru
    rakho a = 10;           # Number (integer)
    rakho b = 10 + (15*20); # Number (expression)
    rakho c = "two";        # String (double quotes)
    rakho d = 'ok';         # String (single quotes)
    rakho f = sach;         # Boolean true
    rakho g = jhoot;        # Boolean false
khatam

5. Variables
5.1 Declaration
Variables are declared using the rakho keyword. DostLang is dynamically typed so the type of a variable can change at any time.

Syntax
rakho <variable_name> = <value>;

Examples
shuru
    rakho a = 10;
    rakho b = "two";
    rakho c = 15;
    rakho name = 'DostLang';
    rakho isReady = sach;
khatam

5.2 Reassignment
Variables can be reassigned without using the rakho keyword. You can also change the type of a variable during reassignment.
shuru
    rakho a = 10;
    a = a + 1;       # Reassign with expression
    a = "now a string"; # Type changed dynamically
khatam

5.3 Variable Rules
•	Must be declared with rakho before use
•	Variable names are case-sensitive
•	Cannot be a reserved keyword (e.g., shuru, khatam, etc.)
•	Can hold any type: number, string, boolean
•	Type can change freely (dynamically typed)
•	Scope: variables declared inside { } blocks are local to that block

6. Operators
6.1 Arithmetic Operators

Operator	Description	Example
+	Addition	a + b
-	Subtraction	a - b
*	Multiplication	a * b
/	Division	a / b
%	Modulo (remainder)	a % b

6.2 Comparison Operators

Operator	Description	Example
==	Equal to	a == b
!=	Not equal to	a != b
<	Less than	a < b
>	Greater than	a > b
<=	Less than or equal to	a <= b
>=	Greater than or equal to	a >= b

7. Built-in Functions
7.1 dikhao — Print to Console
The dikhao function prints one or more values to the output console. It accepts multiple comma-separated arguments of any type.

Syntax
dikhao(<value1>, <value2>, ...);

Examples
shuru
    dikhao("Hello World");         # Print a string
    rakho a = 10;
    {
        rakho b = 20;
        dikhao(a + b);             # Print expression: 30
    }
    dikhao(5, 'ok', sach, jhoot); # Print multiple values
khatam

7.2 Scope Blocks
Curly brace blocks { } can be used anywhere to create a new scope. Variables declared inside a block are only accessible within that block.
shuru
    rakho x = 100;
    {
        rakho y = 200;
        dikhao(x + y);  # OK: 300
    }
    # dikhao(y);       # ERROR: y is out of scope
khatam

8. Conditionals (agar / warna)
DostLang supports conditional execution using agar (if) and warna (else/else-if). Conditions evaluate to sach (true) or jhoot (false).

8.1 Simple if
Syntax
agar (<condition>) {
    # code if condition is sach
}

Example
shuru
    rakho a = 10;
    agar (a < 20) {
        dikhao("a is less than 20");
    }
khatam

8.2 if-else
shuru
    rakho a = 30;
    agar (a < 20) {
        dikhao("less than 20");
    } warna {
        dikhao("20 or more");
    }
khatam

8.3 if-else-if-else (Chained)
shuru
    rakho a = 22;
    agar (a < 20) {
        dikhao("a is less than 20");
    } warna {
        agar (a < 25) {
            dikhao("a is less than 25");
        } warna {
            dikhao("a is 25 or more");
        }
    }
khatam

8.4 Conditional Rules
•	Condition must be enclosed in parentheses: agar (condition)
•	Code block must be enclosed in curly braces { }
•	warna is optional; used for else or else-if
•	warna { agar ... } creates an else-if chain
•	Conditions use comparison operators: <, >, ==, !=, <=, >=

9. Loops (jabtak)
The jabtak keyword implements a while loop. Statements inside the jabtak block execute repeatedly as long as the condition evaluates to sach. When the condition becomes jhoot, the loop terminates.

9.1 Syntax
jabtak (<condition>) {
    # code to repeat
}

9.2 Example
shuru
    rakho a = 0;
    jabtak (a < 10) {
        a = a + 1;
        dikhao(a);
    }
    dikhao("done");
khatam

9.3 Loop Rules
•	Condition must be enclosed in parentheses: jabtak (condition)
•	Code block must be enclosed in curly braces { }
•	Condition is checked BEFORE each iteration (pre-condition loop)
•	If condition starts as jhoot, body never executes
•	Ensure the loop variable is modified inside the loop to avoid infinite loops
•	All comparison operators are valid in loop conditions

10. Functions (kaam / wapas)
Functions are declared using kaam and return values using wapas. Functions support recursion and can be called from anywhere after declaration.

10.1 Syntax
kaam <functionName>(<param1>, <param2>, ...) {
    # function body
    wapas <value>;
}

10.2 Example — Simple Function
shuru
    kaam jama(a, b) {
        wapas a + b;
    }
    rakho result = jama(5, 3);
    dikhao(result);  # Output: 8
khatam

10.3 Recursion Example — Factorial
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

10.4 Function Rules
•	Declare with kaam followed by function name and parameters in parentheses
•	Function body enclosed in curly braces { }
•	wapas returns a value; the function exits immediately
•	Functions can call themselves (recursion is supported)
•	Parameters are passed by value
•	Functions must be defined before being called

11. Array Operations
DostLang supports basic array operations. Arrays are ordered collections of values.

11.1 Array Example
shuru
    rakho arr = [1, 2, 3, 4, 5];
    dikhao(arr[0]);      # Access first element: 1
    arr[2] = 99;        # Modify element
    dikhao(arr[2]);     # Output: 99
khatam

12. Complete Program Example
The following program demonstrates all major features of DostLang:

shuru
    # --- Variables and Types ---
    rakho name = "DostLang";
    rakho version = 1;
    rakho isAwesome = sach;

    # --- Output ---
    dikhao("Welcome to", name, "v", version);

    # --- Conditional ---
    agar (isAwesome == sach) {
        dikhao("DostLang is awesome!");
    } warna {
        dikhao("Keep working!");
    }

    # --- Loop ---
    rakho counter = 1;
    jabtak (counter <= 5) {
        dikhao(counter);
        counter = counter + 1;
    }

    # --- Function & Recursion ---
    kaam factorial(n) {
        agar (n <= 1) {
            wapas 1;
        } warna {
            wapas n * factorial(n - 1);
        }
    }
    dikhao(factorial(6));  # Output: 720

khatam

13. Common Errors & Rules Summary

Rule	Correct Usage
Program must start with shuru	shuru ... khatam
Statements end with semicolon	dikhao("hello");
Declare variables before use	rakho x = 5;
Boolean values are Urdu words	sach / jhoot
Condition needs parentheses	agar (x > 0) { }
Loop needs parentheses	jabtak (x < 10) { }
Comments use # symbol	# this is a comment
Functions declared with kaam	kaam add(a, b) { }
Return value with wapas	wapas a + b;

— End of DostLang Documentation —
