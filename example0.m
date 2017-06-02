(map (1 2 3) print)
(print 1 2 3 nil true false)
(print (1 2 3 nil true false))

(def a 10)
(print a)

(fn f (n s) (
    (+ n s)
))

(print (f 10 20))

(print (reduce (1 2 3) 0 (fn f (n s) (
    (+ n s)
))))

(print (range 5))

(print (map (range 10) (fn f (n) ((* n 2)))))

(print (filter (range 10) (fn f (n) ((% n 2)))))



(fn f (a) (
    (fn g (b) (
        (+ a b)
    ))
))

(def f10 (f 10))
(def b (f10 5))
(print b)

(if (== b 15)
    ((print true) (print true))
    ((print false))
)