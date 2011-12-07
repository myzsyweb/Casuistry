from part3 import Scm
import unittest
class Test(unittest.TestCase):
    def setUp(self):
        self.s = Scm()
        import sys
        sys.setrecursionlimit(200)
    def eval(self,code):
        return self.s.sh(code)
    def evalF(self,code):
        pass
    def equal(self,code,output):
        self.assertEquals(self.s.sh(code),self.s.read(output))

    def test4_1_1(self):
        self.eval(r""" (define x 28) """)
        self.equal(r""" x """,r""" 28 """)
    def test4_1_2(self):
        self.equal(r""" (quote a) """,r""" a """)
        self.equal(r""" (quote #(a b c)) """,r""" #(a b c) """)
        self.equal(r""" (quote (+ 1 2)) """,r""" (+ 1 2) """)
        self.equal(r""" 'a """,r""" a """)
        self.equal(r""" '#(a b c) """,r""" #(a b c) """)
        self.equal(r""" '() """,r""" () """)
        self.equal(r""" '(+ 1 2) """,r""" (+ 1 2) """)
        self.equal(r""" '(quote a) """,r""" (quote a) """)
        self.equal(r""" ''a """,r""" (quote a) """)
        self.equal(r""" '"abc" """,r""" "abc" """)
        self.equal(r""" "abc" """,r""" "abc" """)
        self.equal(r""" '145932 """,r""" 145932 """)
        self.equal(r""" 145932 """,r""" 145932 """)
        self.equal(r""" '#t """,r""" #t """)
        self.equal(r""" #t """,r""" #t """)
    def test4_1_2a(self):
        self.evalF(r""" (set-car! '(1 . 2) 'a) """)
    def test4_1_2b(self):
        self.evalF(r""" (string-set! '"abc" 0 #\b) """)
    def test4_1_2c(self):
        self.evalF(r""" (vector-set! '#(1 2 3) 0 'a) """)
    def test4_1_3a(self):
        self.equal(r""" (+ 3 4) """,r""" 7 """)
        self.equal(r""" ((if #f + *) 3 4) """,r""" 12 """)
    def test4_1_3b(self):
        self.evalF(r""" () """)
    def test4_1_4(self):
        self.equal(r""" ((lambda (x) (+ x x)) 4) """,r""" 8 """)
        self.eval(r""" (define reverse-subtract
      (lambda (x y) (- y x))) """)
        self.equal(r""" (reverse-subtract 7 10) """,r""" 3 """)
        self.eval(r""" (define add4
      (let ((x 4))
        (lambda (y) (+ x y)))) """)
        self.equal(r""" (add4 6) """,r""" 10 """)
    def test4_1_4a(self):
        self.evalF(r""" (lambda (x y x) y) """)
    def test4_1_4b(self):
        self.equal(r""" ((lambda x x) 3 4 5 6) """,r""" (3 4 5 6) """)
        self.equal(r""" ((lambda (x y . z) z) 3 4 5 6) """,r""" (5 6) """)
    def test4_1_5(self):
        self.equal(r""" (if (> 3 2) 'yes 'no) """,r""" yes """)
        self.equal(r""" (if (> 2 3) 'yes 'no) """,r""" no """)
        self.equal(r""" (if (> 3 2)
        (- 3 2)
        (+ 3 2)) """,r""" 1 """)
    def test4_1_6(self):
        self.eval(r""" (define x 2) """)
        self.equal(r""" (+ x 1) """,r""" 3 """)
        self.eval(r""" (set! x 4) """)
        self.equal(r""" (+ x 1) """,r""" 5 """)
    def test4_2_2_let(self):
        self.equal(r""" (let ((x 2) (y 3))
      (* x y)) """,r""" 6 """)
        self.equal(r""" (let ((x 2) (y 3))
      (let ((x 7)
            (z (+ x y)))
        (* z x))) """,r""" 35 """)
    def test4_2_2a_let(self):
        self.evalF(r""" (let ((x 1) (y x)) 0) """)
    def test4_2_2b_let(self):
        self.evalF(r""" (let ((x y) (y 1)) 0) """)
    def test4_2_2a_letstar(self):
        self.equal(r""" (let ((x 2) (y 3))
      (let* ((x 7)
             (z (+ x y)))
        (* z x))) """,r""" 70 """)
    def test4_2_2b_letstar(self):
        self.equal(r""" (let* ((a 1) (b (+ a 1)) (c (+ a b)) (d (+ b c)) (e (+ c d)))  (list a b c d e)) """,r""" (1 2 3 5 8) """)
    def test4_2_2c_letstar(self):
        self.equal(r""" (let* ((x 1) (y x)) y) """,r""" 1 """)
    def test4_2_2d_letstar(self):
        self.evalF(r""" (let* ((x y) (y 1)) 0) """)
    def test4_2_2_letrec(self):
        self.equal(r""" (letrec ((even?
              (lambda (n)
                (if (zero? n)
                    #t
                    (odd? (- n 1)))))
             (odd?
              (lambda (n)
                (if (zero? n)
                    #f
                    (even? (- n 1))))))
      (even? 88))
     """,r""" #t """)
        self.equal(r""" (letrec ((x (lambda () y)) (y (lambda () x))) 0) """,r""" 0 """)
    def test4_2_2_common(self):
        self.equal(r""" (let ((x 1)) (let    () (define x 2) x) x) """,r""" 1 """)
        self.equal(r""" (let ((x 1)) (let*   () (define x 2) x) x) """,r""" 1 """)
        self.equal(r""" (let ((x 1)) (letrec () (define x 2) x) x) """,r""" 1 """)
        self.equal(r""" (let ((x 1)) (begin     (define x 2) x) x) """,r""" 2 """)
    def test4_2_3(self):
        self.eval(r""" (define x 0) """)
        self.equal(r""" (begin (set! x 5)
           (+ x 1)) """,r""" 6 """)
    def test4_2_4_named_let(self):
        self.equal(r""" (let f ((x 3) (y 7))
      (if (= x 0) y (f (- x 1) y))) """,r""" 7 """)
    def test4_2_6(self):
        self.equal(r""" `(list ,(+ 1 2) 4) """,r""" (list 3 4) """)
        self.equal(r""" (let ((name 'a)) `(list ,name ',name)) """,r""" (list a (quote a)) """)
        self.equal(r""" `(a ,(+ 1 2) ,@(list 4 5 6) b) """,r""" (a 3 4 5 6 b) """)
        self.equal(r""" `#(10 5 ,(+ 1 1) ,@(list 4 3) 8) """,r""" #(10 5 2 4 3 8) """)
        self.equal(r""" `(a `(b ,(+ 1 2) ,(foo ,(+ 1 3) d) e) f) """,r""" (a `(b ,(+ 1 2) ,(foo 4 d) e) f) """)
        self.equal(r""" (let ((name1 'x) (name2 'y)) `(a `(b ,,name1 ,',name2 d) e)) """,r""" (a `(b ,x ,'y d) e)) """)
    def test5_2(self):
        self.evalF(r""" (define x 1 2 3) """)
    def test5_2a(self):
        self.evalF(r""" (set! x 1 2 3) """)
    def test5_2b(self):
        self.equal(r""" (begin (define (f x) x x x x x) (f 1)) """,r""" 1 """)
        self.equal(r""" (let ((a 1))  (define (f x)    (define b (+ a x))    (define a 5)    (+ a b))  (f 10)) """,r""" 20 """)
    def test5_3(self):
        self.eval(r""" (define-syntax static-cons   (lambda (def-env use-env . args)    (cons       use-env       (list 'quote (apply cons args))))) """)
        self.equal(r""" (static-cons a b) """,r""" (a . b) """)
    def test6_1a(self):
        self.equal(r""" (eqv? 'a 'a) """,r""" #t """)
        self.equal(r""" (eqv? 'a 'b) """,r""" #f """)
        self.equal(r""" (eqv? 2 2) """,r""" #t """)
        self.equal(r""" (eqv? '() '()) """,r""" #t """)
        self.equal(r""" (eqv? 100000000 100000000) """,r""" #t """)
        self.equal(r""" (eqv? (cons 1 2) (cons 1 2)) """,r""" #f """)
        self.equal(r""" (eqv? (lambda () 1) (lambda () 2)) """,r""" #f """)
        self.equal(r""" (eqv? #f 'nil) """,r""" #f """)
        self.equal(r""" (let ((p (lambda (x) x))) (eqv? p p)) """,r""" #t """)
        self.eval(r""" (define gen-counter   (lambda ()     (let ((n 0))       (lambda ()         (set! n (+ n 1))         n)))) """)
        self.equal(r""" (let ((g (gen-counter))) (eqv? g g)) """,r""" #t """)
        self.equal(r""" (eqv? (gen-counter) (gen-counter)) """,r""" #f """)
        self.equal(r""" (let ((x '(a))) (eqv? x x)) """,r""" #t """)
    def test6_1b(self):
        self.equal(r""" (eq? 'a 'a) """,r""" #t """)
        self.equal(r""" (eq? (list 'a) (list 'a)) """,r""" #f """)
        self.equal(r""" (eq? '() '()) """,r""" #t """)
        self.equal(r""" (eq? car car) """,r""" #t """)
        self.equal(r""" (let ((x '(a))) (eq? x x)) """,r""" #t """)
        self.equal(r""" (let ((x '#())) (eq? x x)) """,r""" #t """)
        self.equal(r""" (let ((p (lambda (x) x))) (eq? p p)) """,r""" #t """)
    def test6_1c(self):
        self.equal(r""" (equal? 'a 'a) """,r""" #t """)
        self.equal(r""" (equal? '(a) '(a)) """,r""" #t """)
        self.equal(r""" (equal? '(a (b) c) '(a (b) c)) """,r""" #t """)
        self.equal(r""" (equal? "abc" "abc") """,r""" #t """)
        self.equal(r""" (equal? 2 2) """,r""" #t """)
        self.equal(r""" (equal? (make-vector 5 'a) (make-vector 5 'a)) """,r""" #t """)
    def testNumbers(self):
        self.equal(r""" (+ 3 4) """,r""" 7 """)
        self.equal(r""" (+ 3) """,r""" 3 """)
        self.equal(r""" (+) """,r""" 0 """)
        self.equal(r""" (* 4) """,r""" 4 """)
        self.equal(r""" (*) """,r""" 1 """)
        self.equal(r""" (+) """,r""" 0 """)
        self.equal(r""" (*) """,r""" 1 """)
        self.equal(r""" (- 1) """,r""" -1 """)
        self.equal(r""" (/ 1) """,r""" 1 """)
        self.equal(r""" (+ 3 3) """,r""" 6 """)
        self.equal(r""" (- 3 3) """,r""" 0 """)
        self.equal(r""" (* 3 3) """,r""" 9 """)
        self.equal(r""" (/ 3 3) """,r""" 1 """)
        self.equal(r""" (+  1 2 3 4) """,r""" 10 """)
        self.equal(r""" (-  1 2 3 4) """,r""" -8 """)
        self.equal(r""" (*  1 2 3 4) """,r""" 24 """)
        self.equal(r""" (/ 24 2 3 4) """,r""" 1 """)
    def test6_3_2(self):
        self.equal(r""" (pair? '(a . b)) """,r""" #t """)
        self.equal(r""" (pair? '(a b c)) """,r""" #t """)
        self.equal(r""" (pair? '()) """,r""" #f """)
        self.equal(r""" (pair? '#(a b)) """,r""" #f """)
        self.equal(r""" (cons 'a '()) """,r""" (a) """)
        self.equal(r""" (cons '(a) '(b c d)) """,r""" ((a) b c d) """)
        self.equal(r""" (cons "a" '(b c)) """,r""" ("a" b c) """)
        self.equal(r""" (cons 'a '3) """,r""" (a . 3) """)
        self.equal(r""" (cons '(a b) 'c) """,r""" ((a b) . c) """)
        self.equal(r""" (car '(a b c)) """,r""" a """)
        self.equal(r""" (car '((a) b c d)) """,r""" (a) """)
        self.equal(r""" (car '(1 . 2)) """,r""" 1 """)
        self.evalF(r""" (car '()) """)
    def test6_3_2a(self):
        self.equal(r""" (cdr '((a) b c d)) """,r""" (b c d) """)
        self.equal(r""" (cdr '(1 . 2)) """,r""" 2 """)
        self.evalF(r""" (cdr '()) """)
    def test6_3_2b(self):
        self.eval(r""" (define (f) (list 'not-a-constant-list)) """)
        self.eval(r""" (define (g) '(constant-list)) """)
        self.eval(r""" (set-car! (f) 3) """)
        self.evalF(r""" (set-car! (g) 3) """)
    def test6_3_2c(self):
        self.eval(r""" (define (f) (list 'not-a-constant-list)) """)
        self.eval(r""" (define (g) '(constant-list)) """)
        self.eval(r""" (set-cdr! (f) 3) """)
        self.evalF(r""" (set-cdr! (g) 3) """)
    def test6_3_2d(self):
        self.equal(r""" (list? '(a b c)) """,r""" #t """)
        self.equal(r""" (list? '()) """,r""" #t """)
        self.equal(r""" (list? '(a . b)) """,r""" #f """)
        self.equal(r""" (list 'a (+ 3 4) 'c) """,r""" (a 7 c) """)
        self.equal(r""" (list) """,r""" () """)
        self.equal(r""" (length '(a b c)) """,r""" 3 """)
        self.equal(r""" (length '(a (b) (c d e))) """,r""" 3 """)
        self.equal(r""" (length '()) """,r""" 0 """)
        self.equal(r""" (append '(x) '(y)) """,r""" (x y) """)
        self.equal(r""" (append '(a) '(b c d)) """,r""" (a b c d) """)
        self.equal(r""" (append '(a (b)) '((c))) """,r""" (a (b) (c)) """)
        self.equal(r""" (append '(a b) '(c . d)) """,r""" (a b c . d) """)
        self.equal(r""" (append '() 'a) """,r""" a """)
        self.equal(r""" (reverse '(a b c)) """,r""" (c b a) """)
        self.equal(r""" (reverse '(a (b c) d (e (f)))) """,r""" ((e (f)) d (b c) a) """)
        self.equal(r""" (memq 'a '(a b c)) """,r""" (a b c) """)
        self.equal(r""" (memq 'b '(a b c)) """,r""" (b c) """)
        self.equal(r""" (memq 'a '(b c d)) """,r""" #f """)
        self.equal(r""" (memq   (list 'a) '(b (a) c)) """,r""" #f """)
        self.equal(r""" (member (list 'a) '(b (a) c)) """,r""" ((a) c) """)
        self.equal(r""" (memv '101 '(100 101 102)) """,r""" (101 102) """)
        self.eval(r""" (define e '((a 1) (b 2) (c 3))) """)
        self.equal(r""" (assq 'a e) """,r""" (a 1) """)
        self.equal(r""" (assq 'b e) """,r""" (b 2) """)
        self.equal(r""" (assq 'd e) """,r""" #f """)
        self.equal(r""" (assq  (list 'a) '(((a)) ((b)) ((c)))) """,r""" #f """)
        self.equal(r""" (assoc (list 'a) '(((a)) ((b)) ((c)))) """,r""" ((a)) """)
        self.equal(r""" (assv 5 '((2 3) (5 7) (11 13))) """,r""" (5 7) """)
        self.equal(r""" (assq 'b '((a . 1) (b . 2))) """,r""" (b . 2) """)
    def test6_3_3(self):
        self.equal(r""" (symbol? 'foo) """,r""" #t """)
        self.equal(r""" (symbol? (car '(a b))) """,r""" #t """)
        self.equal(r""" (symbol? "bar") """,r""" #f """)
        self.equal(r""" (symbol? 'nil) """,r""" #t """)
        self.equal(r""" (symbol? '()) """,r""" #f """)
        self.equal(r""" (symbol? #f) """,r""" #f """)
        self.equal(r""" (symbol->string 'flying-fish) """,r""" "flying-fish" """)
        self.equal(r""" (symbol->string 'Martin) """,r""" "martin" """)
        self.equal(r""" (symbol->string (string->symbol "Malvia")) """,r""" "Malvia" """)
    def test6_3_5(self):
        self.eval(r""" (define (f) (make-string 3 #\*)) """)
        self.eval(r""" (define (g) "***")) """)
        self.eval(r""" (string-set! (f) 0 #\?) """)
        self.evalF(r""" (string-set! (g) 0 #\?) """)
    def test6_3_5a(self):
        self.evalF(r""" (string-set! (symbol->string 'immutable) 0 #\?) """)
    def test6_3_6(self):
        self.equal(r""" (vector-ref '#(1 1 2 3 5 8 13 21) 5) """,r""" 8 """)
        self.equal(r""" (vector 'a 'b 'c) """,r""" #(a b c) """)
        self.equal(r""" (vector-length '#(1 2 3 4)) """,r""" 4 """)
    def test6_4_procedureq(self):
        self.equal(r""" (procedure?  car) """,r""" #t """)
        self.equal(r""" (procedure? 'car) """,r""" #f """)
        self.equal(r""" (procedure?  (lambda (x) (* x x))) """,r""" #t """)
        self.equal(r""" (procedure? '(lambda (x) (* x x))) """,r""" #f """)
        self.equal(r""" (call-with-current-continuation procedure?) """,r""" #t """)
    def test6_4_apply(self):
        self.equal(r""" (apply + (list 3 4)) """,r""" 7 """)
        self.equal(r""" (apply + 1 2 '(3 4)) """,r""" 10 """)
        self.equal(r""" (let ((l (list 1 2)))  (apply    (lambda x (set-car! x 3))    l)  l) """,r""" (1 2) """)
    def test6_4_map(self):
        self.equal(r""" (map + '(1 2 3) '(4 5 6)) """,r""" (5 7 9) """)
    def test6_4_for_each(self):
        self.equal(r""" (let ((v (make-vector 5))       (n 0))   (for-each     (lambda (x y)       (vector-set! v n (+ x y))       (set! n (+ n 1)))     '(0 1 2 3 4)     '(1 1 2 3 5))   v) """,r""" #(1 2 4 6 9) """)
    def test6_4_force(self):
        self.equal(r""" (force (delay (+ 1 2))) """,r""" 3 """)
        self.equal(r""" (let ((p (delay (+ 1 2)))) (list (force p) (force p))) """,r""" (3 3) """)
        self.eval(r""" (begin  (define count 0)  (define x 'foo)  (define p    (delay      (begin        (set! count (+ count 1))        (if (> count x)          count          (force p)))))  (define x 5)) """)
        self.equal(r""" (force p) """,r""" 6 """)
        self.eval(r""" (set! x 10) """)
        self.equal(r""" (force p) """,r""" 6 """)
    def test6_4_callcc(self):
        self.equal(r""" (let ((path '())
          (c #f))
      (let ((add (lambda (s)
                   (set! path (cons s path)))))
        (dynamic-wind
          (lambda () (add 'connect))
          (lambda ()
            (add (call-with-current-continuation
                   (lambda (c0)
                     (set! c c0)
                     'talk1))))
          (lambda () (add 'disconnect)))
        (if (< (length path) 4)
            (c 'talk2)
            (reverse path)))) """,r""" (connect talk1 disconnect connect talk2 disconnect) """)
    def test6_5(self):
        self.equal(r""" (eval '(* 7 3) (scheme-report-environment 5)) """,r""" 21 """)
        self.equal(r""" (let ((f (eval '(lambda (f x) (f x x))
           (null-environment 5))))
      (f + 10)) """,r""" 20 """)



if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(200)
    unittest.main()
