# HPL Core Features Demo

This directory contains example HPL (H Programming Language) scripts that demonstrate the core functionality of the language.

## Files

- `core_features_demo.hpl` - Comprehensive demonstration of all HPL core features

## Running the Demo

```bash
cd h-lang
python run_demo.py
```

Or run specific sections:

```bash
python run_demo.py --section variables
python run_demo.py --section functions
python run_demo.py --section game
```

## Interactive Mode

```bash
python run_demo.py --interactive
```

## Features Demonstrated

### 1. Variables and Assignment
- Basic variables: `set x to 10`
- Global variables: `set $globalVar to 100`

### 2. Data Types
- Numbers (integers and floats)
- Strings with escape sequences
- Booleans (`true`, `false`)
- Null (`null`)
- Lists: `[1, 2, 3]`

### 3. Arithmetic Operations
- Addition, subtraction, multiplication, division, modulo
- Negation: `-42`
- Complex expressions with parentheses

### 4. Comparison Operations
- `is` (equals)
- `is not` (not equals)
- `is greater than` / `>`
- `is less than` / `<`
- `is at least` / `>=`
- `is at most` / `<=`

### 5. Logical Operations
- `and` (logical AND)
- `or` (logical OR)
- `not` (logical NOT)

### 6. Control Flow
- If/else if/else statements
- While loops
- Break/continue support

### 7. Functions
- Function definition: `function name(params):`
- Function calls with arguments
- Return statements
- Recursive functions

### 8. List Operations
- Index access: `list[0]`, `list[-1]`
- Length: `len(list)`
- Contains check: `list contains element`
- Sort: `sort(list)`
- Reverse: `reverse(list)`
- Append: `append(list, element)`
- Index of: `indexOf(list, element)`

### 9. String Operations
- Length: `len(string)`
- Upper/lower case: `upper(string)`, `lower(string)`
- Contains: `contains(string, substring)`
- Starts/ends with: `startsWith(string, prefix)`, `endsWith(string, suffix)`
- Substring: `substring(string, start, length)`
- Split: `split(string, separator)`
- Replace: `replace(string, old, new)`
- Trim: `trim(string)`

### 10. Math Functions
- `floor(number)`
- `ceil(number)`
- `round(number, precision)`
- `abs(number)`
- `max(a, b, c...)`
- `min(a, b, c...)`
- `sqrt(number)`
- `pow(base, exponent)`
- `random()`, `randomInt(min, max)`

### 11. Type Conversion
- `toString(value)`
- `toNumber(value)`
- `toBoolean(value)`
- `toList(value)`

### 12. Special Statements
- `increase variable by amount`
- `decrease variable by amount`
- `ask "prompt" as variable`
- `echo expression`

## Example Code Snippets

### Hello World
```hpl
echo "Hello, World!"
```

### Variables and Math
```hpl
set x to 10
set y to 20
set sum to x + y
echo "Sum: " + sum
```

### Conditionals
```hpl
set temperature to 25
if temperature is greater than 30:
    echo "It's hot!"
else:
    echo "It's not too hot"
```

### Loops
```hpl
set counter to 0
while counter is less than 5:
    echo "Count: " + counter
    increase counter by 1
```

### Functions
```hpl
function greet(name):
    echo "Hello, " + name

greet("World")
```

### Lists
```hpl
set items to ["apple", "banana", "cherry"]
echo items[0]
echo "Length: " + len(items)
```

### Game Logic Example
```hpl
set $playerHealth to 100

function takeDamage(damage):
    decrease $playerHealth by damage
    echo "Health: " + $playerHealth

takeDamage(20)
