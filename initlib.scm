(define list (lambda x x))
(define cdar (lambda (x) (cdr (car x))))
(define cadr (lambda (x) (car (cdr x))))

(define (fold-right p i x)
  (if (null? x) i
      (p (car x) (fold-right p i (cdr x)))))
(define (fold-left p i x)
  (if (null? x) i
      (fold-left p (p i (car x)) (cdr x))))
;(define (map f x)
;  (fold-right (lambda (a b) (cons (f a) b)) '() x))
(define (::map f x)
  (fold-right (lambda (a b) (cons (f a) b)) '() x))
(define (member obj lst)
  (cond
    ((null? lst) #f)
    ((equal? obj (car lst)) lst)
    (else (member  obj (cdr lst)))))
(define (zero? n) (= n 0))
(define (append . x)
  (define (append a b)
    (if (null? a) b
        (cons (car a) (append (cdr a) b))))
  (fold-left append '() x))
(define (length x)
  (fold-right (lambda (a b) (+ b 1)) 0 x))