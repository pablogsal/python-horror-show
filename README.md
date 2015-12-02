Python's horror show
====================

Here you will find a collection of strange and odd python snippets showing apparent odd behavior. The purpose of these scripts is to **mess with your head** but some people have reported strange new **Python knowledge** as a secondary effect.

Hidden memory things
--------------------

```python
>>> a = 5
>>> b = 5
>>> a is b
True

>>> a = -4
>>> b = -4
>>> a is b  
True

>>> a = 300
>>> b = 300
>>> a is b
False

>>> a = 300; b = 300
>>> a is b
True
```

From [7.2.1, "Plain Integer Objects"](http://docs.python.org/c-api/int.html):
> The current implementation keeps an
> array of integer objects for all
> integers between -5 and 256, when you
> create an int in that range you
> actually just get back a reference to
> the existing object. So it should be
> possible to change the value of 1. I
> suspect the behaviour of Python in
> this case is undefined. :-)

We can check this thing using the `id` operator:
```python
>>> a = 5
>>> b = 5
>>> id(a)
4531116864
>>> id(b)
4531116864

>>> a = 300
>>> b = 300
>>> id(a)
4537522896
>>> id(b)
4537523216

>>> a = 300; b = 300
>>> id(a)
4537523696
>>> id(b)
4537523696
```

The brief explanation is that as in Python everything is an object, each time you use a number (integer, float...) **it must be created** so this could be very inefficient. So what Python does is pre-allocate integers from `-5` to `256` because these are often used. The last trick (`a = 300; b = 300`) is interpreter-dependent, but in the basic Python interpreter (among others) as the two assignations occur in the same line both variables will refer to the same object to avoid wasting space.


Indexes for noobs
--------------------

```python

>>> a = [1,2]
>>> a.index(1)
0
>>> a.index(2)
1
>>> a[a.index(1)]
1
>>> a[a.index(2)]
2

>>> a[a.index(1)],a[a.index(2)] = 2,1
>>> a
[1, 2]
```

Woaaaa! WTF is happening here? Easy: we are forgetting that everything must be evaluated sequentially. Let's check this again but one statement after another:
```python

>>> a = [1,2]

>>> a[a.index(1)] = 2
>>> a
[2, 2]
>>> a.index(2)
0
>>> a[a.index(2)] = 1
>>> a
[1, 2]
```

Aha! So the thing is that when we assign `a[a.index(1)] = 2` as `a.index(2)` will give us **the first index in which `2` appears** it gives `1` and therefore `a[a.index(2)] = 1` will reset `a` to its initial value.

Too many equals
--------------------

This is one of my favourites:

```python

>>> a, b = a[b] = {},5
>>> a
{5: ({...}, 5)}
>>> b
5
```

Hummmmmm.... I think the problem with this is that as soon as we see the double equal we think in the formal propositional logic implications of the statement. But as we have seen already, things must be evaluated sequentially. In this case the rules are two:

1. Left before right
2. `a = b = c` is sugar for `a=c & b =c`

So the only thing we have to do in order to undo this mess is execute the code following this rules as
```python
>>> a, b = {},5
>>> a[b] = {},5 # As a is an empty dic and b=5 this is equivalent to {}[5] = ({},5)
>>> a
{5: ({...}, 5)}
>>> b
5
```

Enter the void
---------------

```python
>>> all([])
True
>>> all([[]])
False
>>> all([[[]]])
True
```

When converted too a bool type, `[]` decay into `False` because it's empty, and `[[]]` becomes `True` since it's not empty. Therefore `all([[]])` is equivalent to `all([False])`, and `all([[[]]])` is the same as `all([True])`. As in `all([])` there is no `False` then is trivially `True`.

Consumed by the `iter` method
---------------------------

```python
>>> a = 2, 1, 3
>>> sorted(a) == sorted(a)
True
>>> reversed(a) == reversed(a)
False
```

Unlike `sorted` which returns a list, `reversed` returns an iterator. Iterators compare equal to themselves, but not to other iterators that contain the same values.

```python
>>> b = reversed(a)
>>> sorted(b) == sorted(b)
False
```

The iterator `b` is consumed by the first `sorted` call. Calling `sorted(b)` once `b` is consumed simply returns `[]`.

`False` is the new `True`
---------------------------
```python
>>> False == False in [False]
True
```

Neither the `==` nor the `in` happens first. They're both [comparison operators](https://docs.python.org/3.5/reference/expressions.html#comparisons), with the same precedence, so they're chained. The line is equivalent to `False == False and False in [False]`, which is `True`.

Return to childhood
---------------------------

```python
>>> x = (1 << 53) + 1
>>> x + 1.0 < x
True
```

The value of `x` can be exactly represented by a Python `int`, but not by a Python `float`, which has 52 bits of precision. When `x` is converted from `int` to a `float`, it needs to be rounded to a nearby value. According to the rounding rules, that nearby value is x - 1, which _can_ be represented by a `float`.

When `x + 1.0` is evaluated, `x` is first converted to a `float` in order to perform the addition. This makes its value x - 1. Then `1.0` is added. This brings the value back up to x, but since the result is a float, it is again rounded down to x - 1.

Next the comparison happens. This is where Python differs from many other languages. In C, for instance, if a `double` is compared to an `int`, the `int` is first converted to a `double`. In this case, that would mean the right-hand side would also be rounded to x - 1, the two sides would be equal, and the `<` comparison would be false. Python, however, has special logic to handle comparison between `float`s and `int`s, and it's able to correctly determine that a `float` with a value of x - 1 is less than an `int` with a value of x.
