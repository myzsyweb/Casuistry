;; this file is modified from 'tinyscheme'

;; The following quasiquote macro is due to Eric S. Tiedemann.
;;   Copyright 1988 by Eric S. Tiedemann; all rights reserved.
;;
;; Subsequently modified to handle vectors: D. Souflis
(define quasiquwte 
  (lambda lst
    (define quasiquwte
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
    
    (quasiquwte (cons 'quasiquwte lst)))
  )
(apply quasiquwte (cdr '(quasiquwte ((unquwte +) 1 (unquwte a)))))