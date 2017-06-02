(map (1 2 3) print)
(print 1 2 3 nil true false)
(print (1 2 3 nil true false))

(def a 10)
(print a)

(fn f (n s) (
    (+ n s)
))

(print (f 10 20))

(print (reduce (1 2 3) 0 (fn f (n s) ((+ n s)))))