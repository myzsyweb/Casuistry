(display "hello")
(define and1 
  (lambda lst 
    (if (null? lst) #t
        (if (null? (cdr lst)) (car lst)
        (list 'if (car lst) (cons 'and (cdr lst))#f))))
  )
(apply and1 '())
(apply and1 '(4))
(apply and1 '((> 4 2) 6))
(apply and1 '((> 4 2) #t #f))
(apply and1 '((> 4 2) 3 #f 5))
(define or1 
  (lambda lst 
    (if (null? lst) #f
        (if (null? (cdr lst)) (car lst)
        (list (list 'lambda (list '::) (list 'if ':: ':: (cons 'or (cdr lst)))) (car lst))   
        )))
  )
(apply or1  '())
(apply or1  '(4))
(apply or1  '((> 4 2) 6))
(apply or1  '((> 4 2) #t #f))
(apply or1  '((> 4 2) 3 #f 5))
;; this file is modified from 'tinyscheme'

;; The following quasiquote macro is due to Eric S. Tiedemann.
;;   Copyright 1988 by Eric S. Tiedemann; all rights reserved.
;;
;; Subsequently modified to handle vectors: D. Souflis
(define quasiquwteex 
  (lambda lst
    ;(display lst)
    (define xquasiquwte
      (lambda (l)
        (define (mcons f l r)
          (if (and (pair? r)
                   (eq? (car r) 'quwte)
                   (eq? (car (cdr r)) (cdr f))
                   (pair? l)
                   (eq? (car l) 'quwte)
                   (eq? (car (cdr l)) (car f)))
              (if (or (procedure? f) (number? f) (string? f))
                  f
                  (list 'quwte f))
              (if (eqv? l vector)
                  (apply l (eval r))
                  (list 'cons l r)
                  )))
        (define (mappend f l r)
          (if (or (null? (cdr f))
                  (and (pair? r)
                       (eq? (car r) 'quwte)
                       (eq? (car (cdr r)) '())))
              l
              (list 'append l r)))
        (define (foo level form)
          (cond ((not (pair? form))
                 (if (or (procedure? form) (number? form) (string? form))
                     form
                     (list 'quwte form))
                 )
                ((eq? 'quasiquwte (car form))
                 (mcons form ''quasiquwte (foo (+ level 1) (cdr form))))
                (#t (if (zero? level)
                        (cond ((eq? (car form) 'unquwte) (car (cdr form)))
                              ((eq? (car form) 'unquwte-splicing)
                               (error "Unquwte-splicing wasn't in a list:"
                                      form))
                              ((and (pair? (car form))
                                    (eq? (car (car form)) 'unquwte-splicing))
                               (mappend form (car (cdr (car form)))
                                        (foo level (cdr form))))
                              (#t (mcons form (foo level (car form))
                                         (foo level (cdr form)))))
                        (cond ((eq? (car form) 'unquwte)
                               (mcons form ''unquwte (foo (- level 1)
                                                          (cdr form))))
                              ((eq? (car form) 'unquwte-splicing)
                               (mcons form ''unquwte-splicing
                                      (foo (- level 1) (cdr form))))
                              (#t (mcons form (foo level (car form))
                                         (foo level (cdr form)))))))))
        (foo 0 (car (cdr l)))))              
    
     (xquasiquwte (cons 'quasiquwte lst)))
  )
(display (apply quasiquwteex (cdr '(quasiquwte ((unquwte +) 1 (unquwte a))))))
(apply quasiquwteex (cdr '(quasiquwte ((unquwte +) 1 (unquwte a)))))
(apply quasiquwteex '(((unquwte +) 1 (unquwte a))))
(apply (lambda x x) '(1 2 3))
(apply quasiquwteex '((1 2 3)))
(display (apply quasiquwteex '((a 2 3))))
(display "should be")
(display '(cons (quwte a) (cons 2 (cons 3 (quwte ())))))
(newline)
(display (apply quasiquwteex '(((unquwte a) 2 3))))
(display '(quwte (a)))
(apply quasiquwteex '((a)))

(define let*1 
  (lambda (h . t) 
    (if (null? h) `(begin . ,t)
        `(let (,(car h)) (let* ,(cdr h) . ,t))))
  )
(display (apply let*1 (cdr ' (let* ()1 2 3))))
(display (apply let*1 (cdr ' (let* ((a 1))1 2 3))))
(display (apply let*1 (cdr ' (let* ((a 1)(b 2))1 2 3))))
(define letrec1 
  (lambda (h . t) 
    `((lambda () ,@(map (lambda (x) `(define . ,x)) h) . ,t)))
        )
   
 
(display (apply letrec1 (cdr ' (letrec ()1 2 3))))
(display (apply letrec1 (cdr ' (letrec ((a 1))1 2 3))))
(display (apply letrec1 (cdr ' (letrec ((a 1)(b 2))1 2 3))))
(define if1 (lambda (e t . f)
  (cons '::if (cons e (cons t (if (null? f) (cons '() '()) f)))))
  )
(apply if1 (cdr' (if 0 1 2)))
(apply if1 (cdr ' (if 0 1)))
#(apply if1 (cdr' (if 0)))
(apply if1 (cdr' (if 0 1 2 4)))

(define let1 
  (lambda lst
            (apply 
             (lambda (name bind . stmt)
               (display name)
               (list (list 'lambda (list)(cons 'define (cons (cons name (if (null? bind) '() (map car bind))) stmt))
                           (cons name (if (null?  bind) '() (map cadr bind))))))
             (if (symbol? (car lst)) lst (cons ':: lst) )))
        )
(display (apply let1 (cdr ' (let () 1 2 3))))
(display (apply let1 (cdr ' (let ((a 1))1 2 3))))
(display (apply let1 (cdr ' (let ((a 1)(b 2))1 2 3))))
(display (apply let1 (cdr ' (let loop () 1 2 3))))
(display (apply let1 (cdr ' (let loop ((a 1))1 2 3))))
(display (apply let1 (cdr ' (let loop ((a 1)(b 2))1 2 3))))
(define do1 
  (lambda (vars endtest . body)
             (let ((do-loop '::))
               `(letrec ((,do-loop
                           (lambda ,(map (lambda (x)
                                           (if (pair? x) (car x) x))
                                      `,vars)
                             (if ,(car endtest)
                               (begin ,@(cdr endtest))
                               (begin
                                 ,@body
                                 (,do-loop
                                   ,@(map (lambda (x)
                                            (cond
                                              ((not (pair? x)) x)
                                              ((< (length x) 3) (car x))
                                              (else (car (cdr (cdr x))))))
                                       `,vars)))))))
                  (,do-loop
                    ,@(map (lambda (x)
                             (if (and (pair? x) (cdr x))
                               (car (cdr x))
                               '()))
                        `,vars)))))
  )
(apply do1 (cdr ' (do ((i 1 (+ i 1))(s 0 (+ s i)))((> i 100)s))
            ))