(def x (1 2 3 4 5))
(print x)

(fn f (n) (
    (* n 2)
))

(def y (map x f))
(print y)

(fn f (a) (
    (lambda (b) (
        (* a b)
    ))
))

(def f10 (f 10))
(def f20 (f 20))
(def f30 (f 30))
(print (f10 5))
(print (f20 5))
(print (f30 5))

(def h (lambda (n) (
    (** n n))
))

(print (h 10))