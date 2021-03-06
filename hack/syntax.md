
# Syntax


## Simple Values

```
a = null            // null
b = true || false   // bool
c = -1 + 0.333      // int and float
d = 'some string'   // str
```


## Collections

```
a = [0, 1, null] + []                   // list
b = {-2, true, false} + {/}             // set
c = {'a': a, 'b': b, 'c': null} + {}    // dict
d = {a = 'a'; b = 'b'; c = 'c'}         // dict
```

## Functions

Last expressions is return value:
```
f = (x, y) -> {x + y}
```

Function call:
```
a = f(10, 20)
```


## Objects

Setting attribute, instead of modifying initial object, creates new object with
attribute set inside of it, so initial object is unmodified.

```
a = {
    x = 10
    y = []
    z = {}
}

x = a.x
a = (a.x = 10)
a = setattr(a, 'x', 10)

b = {
    x = {
        y = {
            z = 10
        }
    }
}

b = b.x = b.x.y = b.x.y.z = 20

b = b.x = b.x.y = {z = 20}
b = setattr(b, 'x', setattr(b.x, 'y', {z = 20}))
```


## Conditional - if, else, match

If/else:
```
x = 10

a = x % 2 ? {true} : {null}

// or
x % 2 ? {
    a = true
} : {
    a = null
}

// or
x % 2 ? {a = true} : {a = null}
```


## Loops - while, for-in

While loop:
```
f = (n) -> {
    a = 0

    a < n @ {
        a = a + 1
    }
}

f(10)
```

Generator:
```
range = (b, e, s) -> {
    b < e ? {
        [b, (_) -> range(b + s, e, s)]
    } : {
        [null, null]
    }
}

range = (b, e, s) -> {
    b < e ? {[b, (_) -> range(b + s, e, s)]} : {[null, null]}
}

range = (b, e, s) -> {b < e ? {[b, (_) -> range(b + s, e, s)]} : {[null, null]}}
```

Manual loop iteration:
```
i, next = range(0, 10, 2)

next != null @ {
  i, next = g()
}
```

Auto loop iteration - for-in:
```
range(0, 10, 2) -> i @ {
    i
}
```


## map, filter, reduce

```
items = range(0, 10, 2)
items = map(items, (n) -> {n / 2})
items = filter(items, (n) -> {n % 2})
result = reduce(items, 0, (accu, n) -> {accu + n})
```
