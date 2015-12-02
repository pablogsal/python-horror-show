Python Wat
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
1
>>> a.index(2)
2
>>> a[a.index(1)]
1
>>> a[a.index(2)]
2

>>> a[a.index(1)],a[a.index(2)] = 2,1
>>> a
[1, 2]
```

Woaaaa! WTF is happening here? Easy: we are forgetting that everything must be evaluated sequentially. Let's see this one statement after another:
```python

>>> a = [1,2]

>>> a[a.index(1)] = 2
>>> a
[2, 2]
>>> a.index(2)
1
>>> a[a.index(2)] = 1
>>> a
[1, 2]
```

Aha! So the thing is that when we assign `a[a.index(1)] = 2` as `a.index(2)` will give us **the first index in which `2` appears** it gives `1` and therefore `a[a.index(2)] = 1` will reset `a` to its initial value.
