(defmarco if (e t . f)
  (cons '::if (cons e (cons t (::if (null? f) (cons '() '()) f)))))
(defmarco define lst
                 (if (pair? (car lst))
                     (cons '::define (cons (car (car lst)) (cons (cons 'lambda (cons (cdr (car lst)) (cdr lst))) '())))
                     (cons '::define lst)))
(defmarco begin lst 
                    (cons '::begin lst))
(defmarco cond (h . t)
                (if (eq? (car h) 'else)
                    (if (null? t)
                        (cons 'begin (cdr h))
                        (error "ELSE isn't last"))
                    
                    (list 'if (car h)
                          (cons 'begin (cdr h))
                          (if (null? t) 
                              '()
                              (cons 'cond t)))))
(defmarco case lst 
              (define expand-rest-case (lambda (lst)
              (if (null? lst)
                  (list 'quote '())
                  (if (eq? (car (car lst)) 'else)
                      (if (null? (cdr lst))
                          (cons 'begin (cdr (car lst)))
                          (error "ELSE isn't last"))
                      (list 'if (list 'member ':: (list 'quote (car (car lst))))
                            (cons 'begin (cdr (car lst)))
                            (expand-rest-case (cdr lst)))))))
            (list (list 'lambda '(::) (expand-rest-case (cdr lst)))(car lst)))
(defmarco let lst
            (apply 
             (lambda (name bind . stmt)
               (list (list 'lambda (list)(cons 'define (cons (cons name (map car bind)) stmt))
                           (cons name (map cadr bind)))))
             (if (pair? (car lst)) (cons ':: lst) lst)))
(defmarco and lst 
    (if (null? lst) #t
        (if (null? (cdr lst)) (car lst)
        (list 'if (car lst) (cons 'and (cdr lst))#f))))
(defmarco or lst 
    (if (null? lst) #f
        (if (null? (cdr lst)) (car lst)
        (list (list 'lambda (list '::) (list 'if ':: ':: (cons 'or (cdr lst)))) (car lst))   
        )))