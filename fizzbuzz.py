# fun w/ fizzbuzz -- short one-liners as functions -- see comments for non-function one-liner.

# 1.) as short as possible; works w/ default fizzbuzz %3 %5 settings


def fizzbuzz(r):
    return ['FizzBuzz'[i**2%3*4:8--i**4%5] or i for i in range(1, r+1)]


'''
FizzBuzz is an 8 character string (w/ indices 0 through 7)
The function above runs the classic 'FizzBuzz' test up to a given value, set by the argument.
The result is a list where each element is either a slice of the FizzBuzz string or the current value of an iterator
The function slices the FizzBuzz string in the following way:
    Any modulo operation on a number, x, where [ (x**(n-1))%n ], and where n is prime, will return a 1 or 0.
    As 3 is prime, the current value of the iterator can be squared and evaluated in the mod expression for a 1 or 0.
    The 1 or 0 is then multiplied by 4 to give a 0 or 4 result, allowing the left side of the string slice to be 0 or 4.
    The number 5 is also prime, so the same x**(n-1)%n = 1 or 0 remains true for the right half of the string slice.
    However, instead of using only the mod result on the string slice, subtract the result of a negative mod from 8.
    Subtracting from 8 allows for 8 to be the upper limit on the right side of the string slice.
    Additionally, when given a negative mod operation, python returns the "inverse" of usual expected result.
    In this case, -x**(5-1)%5 returns 4 or 0 instead of 1 or 0.
     -- note:  Could do the same thing as on the left side, multiplying by 4 etc., but it is shorter this way.
    Subtracting the result of the negative mod from 8 will yield either 8 or 4 for the right side of the string slice.
    The remaining potential outcomes are now:
        'FizzBuzz'[0:4] --> 'Fizz'
        'FizzBuzz'[4:4] --> ''
        'FizzBuzz'[4:8] --> 'Buzz'
        'FizzBuzz'[0:8] --> 'FizzBuzz'
In the event of an empty string ('FizzBuzz'[4:4]), the function above will return the current value of the iterator.
Iteration continues until the range specified as the argument to the function is met.

One liner w/ default settings: (divisible by 3 & 5, range of 1 to 100 [60 chars]:
['FizzBuzz'[i**2%3*4:8--i**4%5] or i for i in range(1, 101)]

Possible to make it one character shorter by using i*i instead of i**2 [59 chars]:
['FizzBuzz'[i*i%3*4:8--i**4%5] or i for i in range(1, 101)]
-----------------------------------------------------------------------------------------------------------------------
'''

# 2.) a bit longer, but works with all positive integers


def fb_any(a, b, r):
    return ['FizzBuzz'[(1 if i % a else 0) * 4:8-((1 if i % b else 0) * 4)] or i for i in range(1, r + 1)]

'''
Nearly the same as the previous FizzBuzz, except that any positive integers may be used.
Uses ternary operators to evaluate mods of 'a' and 'b'.
Also, spaced everything out PEP8 style...

One liner w/ default settings: (divisible by 3 & 5, range of 1 to 100) [89 chars]:
['FizzBuzz'[(1 if i % 3 else 0)*4:8-((1 if i % 5 else 0)*4)] or i for i in range(1, 101)]
-----------------------------------------------------------------------------------------------------------------------
'''
