
(fn irange (b e s) (
    ; ? {
    ;     b < e -> [b, (_) -> range(b + s, e, s)]}
    ;     _ -> [null, null]
    ; }
    (if (< b e) (
        (b (lambda () (irange (+ b s) e s)))
    ) (
        (null null)
    ))
))


; i, next = irange(0 10 1)
(def g (irange 0 10 1))
(print g)

(def n (get g 1))
(print n)
(def g (n))
(print g)
