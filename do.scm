;from tinyscheme
(defmarco do (vars endtest . body)
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