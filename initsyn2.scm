(defmarco let* (h . t) 
    (if (null? h) `(begin . ,t)
        `(let (,(car h)) (let* ,(cdr h) . ,t))))
(defmarco letrec (h . t) 
    `((lambda () ,@(map (lambda (x) `(define . ,x)) h) . ,t)))