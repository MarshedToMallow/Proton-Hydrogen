# The Proton Programming Language

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