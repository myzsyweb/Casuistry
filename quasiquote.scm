;; Macro `quasiquote' is modified from 'tinyscheme'
;; The following quasiquote macro is due to Eric S. Tiedemann.
;;   Copyright 1988 by Eric S. Tiedemann; all rights reserved.
;; Subsequently modified to handle vectors: D. Souflis
(defmarco quasiquote lst
  (define xquasiquote
    (lambda (l)
      (define (mcons f l r)
        (if (and (pair? r)
                 (eq? (car r) 'quote)
                 (eq? (car (cdr r)) (cdr f))
                 (pair? l)
                 (eq? (car l) 'quote)
                 (eq? (car (cdr l)) (car f)))
            (if (or (procedure? f) (number? f) (string? f))
                f
                (list 'quote f))
            (if (eqv? l vector)
                (apply l (eval r))
                (list 'cons l r)
                )))
      (define (mappend f l r)
        (if (or (null? (cdr f))
                (and (pair? r)
                     (eq? (car r) 'quote)
                     (eq? (car (cdr r)) '())))
            l
            (list 'append l r)))
      (define (foo level form)
        (cond ((not (pair? form))
               (if (or (procedure? form) (number? form) (string? form))
                   form
                   (list 'quote form))
               )
              ((eq? 'quasiquote (car form))
               (mcons form ''quasiquote (foo (+ level 1) (cdr form))))
              (#t (if (zero? level)
                      (cond ((eq? (car form) 'unquote) (car (cdr form)))
                            ((eq? (car form) 'unquote-splicing)
                             (error "Unquote-splicing wasn't in a list:"
                                    form))
                            ((and (pair? (car form))
                                  (eq? (car (car form)) 'unquote-splicing))
                             (mappend form (car (cdr (car form)))
                                      (foo level (cdr form))))
                            (#t (mcons form (foo level (car form))
                                       (foo level (cdr form)))))
                      (cond ((eq? (car form) 'unquote)
                             (mcons form ''unquote (foo (- level 1)
                                                        (cdr form))))
                            ((eq? (car form) 'unquote-splicing)
                             (mcons form ''unquote-splicing
                                    (foo (- level 1) (cdr form))))
                            (#t (mcons form (foo level (car form))
                                       (foo level (cdr form)))))))))
      (foo 0 (car (cdr l)))))              
  (xquasiquote (cons 'quasiquote lst)))






