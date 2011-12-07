;from Yet Another Scheme Tutorial.    
;;; queue
(define (make-queue)
  (cons '() '()))

(define (enqueue! queue obj)
  (let ((lobj (list obj)))
    (if (null? (car queue))
        (begin
          (set-car! queue lobj)
          (set-cdr! queue lobj))
        (begin
          (set-cdr! (cdr queue) lobj)
          (set-cdr! queue lobj)))
    (car queue)))

(define (dequeue! queue)
  (let ((obj (car (car queue))))
    (set-car! queue (cdr (car queue)))
    obj))


;;; coroutine   
(define process-queue (make-queue))

(define (coroutine thunk)
  (enqueue! process-queue thunk))

(define (start)
  ((dequeue! process-queue)))

(define (pause)
  (call-with-current-continuation
   (lambda (k)
     (coroutine (lambda () (k #f)))
     (start))))


;;; example
(coroutine (lambda ()
             (let loop ((i 0)) 
               (if (< i 10)
                   (begin
                     (display (+ 1 i)) 
                     (display " ") 
                     (pause) 
                     (loop (+ 1 i)))))))

(coroutine (lambda ()
             (let loop ((i 0)) 
               (if (< i 10)
                   (begin
                     (display (integer->char (+ i 97)))
                     (display " ")
                     (pause) 
                     (loop (+ 1 i)))))))

(newline)
(start)