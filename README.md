# Hydrogen - The first Proton Interpreter

Hydrogen is the name of the interpreter and Proton is the name of the programming language that Hydrogen can run code for.  
The information here is largely about Proton rather than Hydrogen, but there is a section below regarding Hydrogen.

## Disclaimers

1. I am far from an expert regarding programming langauge design, compiler/interpreter design, or programming in general
2. Proton is first and foremost for me, so any changes are my decisions and are intended to improve my own experience with the language
    - This does not mean I will entirely ignore suggestions and feedback, but rather that the final decisions on those are my call
3. The license is currently not included, but will hopefully be worked out soon

# What is Proton?

Proton is:
- Similar in syntax to Python
- Strongly typed
- Numerically exact*

## What's with the asterisk after "Numerically exact"?

That last point is one of my main motivations with Proton.  
All Proton programs execute the same as one with theoretically exact numeric precision.

In most languages, there are integers and floats and hard limits on the scale and precision of those numbers.  
Proton's limits exist (there's still finite memory of course), but it aims to be efficient where possible and as exact as it can be.

As an example, consider the code below:

```
a: real = 2.528
if sin(a) > 2:
  print("Hi")
```

A typical program would compute the sine of `a` and compare that against 2, but Proton wouldn't even begin to compute it.  
Proton includes the domain and range of functions, so it knows that `sin.range == [-1,1]` and `sin.range < 2`  
That means before any actual computation takes place, it knows the print statement will never happen.

I hope to gradually improve the way Proton handles comparisons and such to the extent possible.  
A mixture of clever tricks and existing CAS (Computer Algebra System) techniques is hopefully enough to get things where I'd like, though I'm far from an expert.

# Interpreters and Compilers

Until a programming language can be run, it's just a specification.  
Below are my current plans regarding the actual execution of Proton programs.

## Hydrogen - The First Proton Interpreter

Hydrogen is the first interpreter for Proton, intended as the messy, unoptimized alpha version.  
Once Hydrogen is in a somewhat stable state, I'll take what I've learned there are map out a plan for Helium.

Hydrogen is written in Python, since that's the programming language I'm most familiar with.  
It isn't meant to be fast or efficient, just functional and enough to test the language with or write some useable programs.

## Helium - The First Proton Compiler

Where Hydrogen is intended as an alpha build, Helium aims to be a more solid and optimized build.  
Additionally, Helium will be a compiler rather than an interpreter.  
It's likely that it'll compile to LLVM, since that enables widespread support with the various existing backends, but the details are something I'll leave for my future self to determine.

## After Helium

Any future interpreters or compilers will follow the naming convention of the next element by atomic number.  

The versioning system isn't determined yet, but will be by the time Helium is started.  
Until then, Hydrogen is likely to have regular compatability-breaking changes as the language features are worked out.  
It is likely that language features will only change drastically after Hydrogen when a new named interpreter or compiler is created.

# The Proton Specification

At present, Proton is not well-defined and is considered volitile while Hydrogen is in development.  
The full specification will be in a somewhat stable form in time for Helium.  
Below are an unorganized collection of my current idea of Proton.

## Variables and Data Types

**Reals**
```
a: real = 2
b: real = -1.6
c: real = 10.8(3)

discriminant: real = b^2 - 4*a*c

if discriminant < 0: // 0 Real Roots
    print("No real solutions")
    halt
elif discriminant == 0: // 1 Real Root
    x: real = -b / (2*a)
    print(f"x = {x}")
else: // 2 Real Roots
    x1: real = (-b - sqrt(discriminant)) / (2*a)
    x2: real = (-b + sqrt(discriminant)) / (2*a)
    print(f"x = {x1} and {x2}")
```

**Booleans**
```
a: bool = false
b: bool = true

if a and b:
    print("Both")
elif a xor b:
    print("One")
else:
    print("None")
```

**Strings**
```
greeting: str = "Hello, World!"
print(greeting)
```

**Segments**
```
real_numbers: seg = [-inf,+inf]
if 5 in real_numbers:
    print("Sounds about right")
else:
    print("what")
```

**Vectors**
```
numbers: vec = [0, 0.5, 8, 4.1]
difference: vec = diff(numbers)

if 0 in difference:
    print("Two elements are identical")
```

**Arrays**
```
point_a: arr[real,3] = [3.2, 0.1, 0.9]
point_b: arr[real,3] = [1, 1.2, 1.5]

distance: real = dist(point_a, point_b)
print(f"There are {distance}m remaining")
```

```
xy: vec2[real] = [0.(3), -0.5]
xyz: vec3[real] = [3.2, -0.1, 0.9]
wxyz: vec4[real] = [0.01, -9, -5.4, 1.19]
```

## Conditionals

```
x: real = 50
if x < 10:
    print("Below 10")
elif x < 100:
    print("Below 100")
else:
    print("Beyond double digit")
```

## Loops

The following two loops run the same number of iterations

```
for i in 10:
    print(i)
```

```
for i in 0..9:
    print(i)
```

```
while true:
    print("help im trapped in a ")
```

## Match Case

```
name: str = "Mallow"
match name case "Bob":
    print("Lovely to meet you, Bob")
case "Mallow":
    print("I'd love to get to know you s'more, Mallow")
else:
    print("I'm not sure what to say, that's an interesting name")
```

## Functions

```
fn factorial(n: int[0,+inf]) -> int:
    if n == 0 or 1:
        return 1
    return n * factorial(n - 1)
```

```
fn primes() -> int[2,+inf]:
    yield 2
    n: int = 3
    while true:
        for p in primes():
            if p * p > n:
                yield n
                break
            if n % p == 0:
                break
        n += 2
```

## Objects

```
thing Sphere:
    fn _on_create(position: vec3[real]) -> Sphere:
        .position = position
```