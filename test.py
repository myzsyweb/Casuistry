from part3 import Scm
import unittest
class Test(unittest.TestCase):
    def setUp(self):
        self.s = Scm()
        import sys
        sys.setrecursionlimit(200)
    def testBase(self):
        self.assertEqual(self.s.sh("1"), 1)
        self.assertEqual(self.s.sh("(+ 1 1)"), 2)
        self.assertEqual(self.s.sh("((lambda (x) (+ x 1)) 7 )"), 8)
        self.assertEqual(self.s.sh("(if (> 1 2) 3 4)"), 4)
        self.assertEqual(self.s.sh("((lambda () (define x 1) x))"), 1)
        self.assertEqual(self.s.sh("((lambda (p) (p 1))(lambda (x) (+ x 1)))"), 2)
        self.assertEqual(self.s.sh("""((lambda x (+ (car x) (car (cdr x)))) 1 2)"""), 3)
        
    def testRead(self):
        self.assertEqual(len(self.s.read("(+ 1 4)").toPyList()),3)
        self.assertEqual(len(self.s.read("'`',a").toPyList()),2)
        self.assertEqual(len(self.s.read("`(12 2 5)").toPyList()),2)
        self.assertEqual(len(self.s.read("`(,12 ,2 ,5)").toPyList()),2)
        self.assertEqual(len(self.s.read("`(12 ,@(+ 2 a) 5)").toPyList()),2)
        self.assertEqual(len(self.s.read("""
                                        (
                                        1;hello
                                        2;world
                                        3)
                                        """).toPyList()),3)
        self.assertEqual(self.s.read("`(,+ ,a 1)"),
            self.s.read("(quasiquote ((unquote +) (unquote a) 1))"))
        self.assertEqual(self.s.read("`(12 ,@(+ 2 a) 5)"),
            self.s.read("(quasiquote (12 (unquote-splicing (+ 2 a)) 5 ))"))
        self.assertEqual(self.s.read("#t"),True)
        self.assertEqual(self.s.read("#f"),False)
        self.assertEqual(self.s.read(r"#\a"),"a")
        self.assertEqual(self.s.read(r"#\A"),"A")
        self.assertEqual(self.s.read(r"#\("),"(")
        self.assertEqual(self.s.read(r"#\ ")," ")
        self.assertEqual(self.s.read(r"#\space")," ")
        self.assertEqual(self.s.read(r"#\newline"),"\n")

    def testType(self):
        self.assertTrue(self.s.sh("(pair? (quote (+ 1 2)))"))
        
    def testOther(self):
        self.assertEqual((self.s.sh("(lambda (x) (+ x 1))"))(1), 2)
    
    def testCont(self):
        self.assertEqual(self.s.sh("""(call/cc (lambda (c) (display "show") (c 1) (display "hide") 2))"""), 1)
        
    def testTailCall(self):
        print self.s.sh("""((lambda ()(define f (lambda (n s) (if (< n 1) s (f (- n 1) (* n s)))))(f 1000 1)))""")

    def testEqual(self):
        self.assertTrue(not self.s.sh("(eqv? 'a 'b)"))
        self.assertTrue(self.s.sh("(eqv? 'a 'a)"))
        self.assertTrue(self.s.sh("(equal? '(1 2) '(1 2))"))
        self.assertTrue(self.s.sh("(= 1 1)"))
    def testEq(self):
        self.assertTrue(self.s.sh("(eq? 'a 'a) "))
        self.assertTrue(not self.s.sh("(eq? (list 'a) (list 'a))"))
        self.assertTrue(self.s.sh("(eq? '() '())"))
        self.assertTrue(self.s.sh("(eq? car car)"))
        self.assertTrue(self.s.sh("(let ((x '(a)))(eq? x x))"))
        self.assertTrue(self.s.sh("(let ((p (lambda (x) x)))(eq? p p))"))


    def testEqv(self):
        self.assertTrue(self.s.sh("(eqv? 'a 'a) "))
        self.assertTrue(not self.s.sh("(eqv? 'a 'b)"))
        self.assertTrue(self.s.sh("(eqv? 2 2)"))
        self.assertTrue(self.s.sh("(eqv? '() '())"))
        self.assertTrue(self.s.sh("(eqv? 100000000 100000000)"))
        self.assertTrue(not self.s.sh("(eqv? (cons 1 2) (cons 1 2))"))
        self.assertTrue(not self.s.sh("(eqv? (lambda () 1)(lambda () 2))"))
        self.assertTrue(not self.s.sh("(eqv? #f 'nil)"))
        self.assertTrue(self.s.sh("(let ((p (lambda (x) x)))(eqv? p p))"))

    def testMarco(self):
        self.assertEqual(self.s.sh("""((lambda ()(define (f x) (+ x 1))(f 4)))"""), 5)
        self.assertEqual(self.s.sh("""(begin (display 1) (display 2) 3)"""), 3)
        self.assertEqual(self.s.sh("""(let loop ((x 10))(if (< x 0) 0 (+ x (loop (- x 1)))))"""), 55)
        self.assertEqual(self.s.sh("""(cond((= 1 2) 3)((= 4 5) 6)(else 7))"""), 7)
        self.assertEqual(self.s.sh("""(begin (cond((= 1 2) 3)((= 4 5) 6)) 7)"""), 7)
        self.assertEqual(self.s.sh("""(case (+ 1 1)((1) 1)((2) 2))"""), 2)

        
    def testTodo(self):
        print self.s.sh("(lambda (x) (+ x 1))")
        print self.s.sh("((lambda ()(define f (lambda (x) (+ x 1)))f))")
        print self.s.sh("call/cc")
        "(display 1)"
    def testFrac(self):
        code = """
            ((lambda ()
                (define fac
                  (lambda (x)
                    (if (> x 0) 
                        (* x (fac (- x 1)))
                        1)))
                (fac 6)))
        """
        self.assertEqual(self.s.sh(code), 720)
        code = """((lambda ()
                    (define (fac x)
                        (if (> x 0) 
                            (* x (fac (- x 1)))
                            1))
                    (fac 6)
                    ))"""                           
        self.assertEqual(self.s.sh(code), 720)

    def testSome(self):
        self.assertEqual(self.s.sh("""(+ 1 6)"""), 7)
        self.assertEqual(self.s.sh("""((lambda (x) (+ x 1)) 7 )"""), 8)
        self.assertEqual(self.s.sh("""((lambda (x y) (+ x y)) 1 9)"""), 10)
        self.assertEqual(self.s.sh("""((lambda () (define x 1) (+ x 2)))"""), 3)
        self.assertEqual(self.s.sh("""((lambda () (define x 1) (if (> 1 2) x (+ x 6))))"""), 7)
        self.assertEqual(self.s.sh("""(car (cdr '(1 . (2 3))))"""), 2)                  
        self.assertEqual(self.s.sh("""(cdr '(1 . 2))"""), 2)
        self.assertEqual(len(self.s.read("""'(1 2 3)""").toPyList()), 2)
        self.assertEqual(len(self.s.sh("""'(1 2 3)""").toPyList()), 3)
        self.assertEqual(self.s.sh("""(cadr (member 2 '(1 2 3)))"""), 3)
        self.assertTrue(not self.s.sh("""(member 4 '(1 2 3))"""))
        self.assertEqual(self.s.sh("""(apply + (map (lambda (x) (+ x 1)) '(0 1 2 3 4)))"""),15)
        
    def testApply(self):                         
        self.assertEqual(self.s.sh("""((lambda (x) (+ (car x) (car (cdr x)))) '(1 2))"""), 3)
        self.assertEqual(self.s.sh("""((lambda x (+ (car x) (car (cdr x)))) 1 2)"""), 3)
        self.assertEqual(self.s.sh("""(apply + '(1 2))"""), 3)
        self.assertEqual(self.s.sh("""(apply (lambda (x . y) (+ x (car y))) '(1 2))"""), 3)
        self.assertEqual(self.s.sh("""((lambda ()(define (f x) (+ x 1))(f 4)))"""), 5)
    def testString(self):
        pass

    def testAppend(self):
        self.assertTrue(self.s.sh("""(null? (append))"""))
        self.assertEqual(len(self.s.sh("(append '(1 2) '(3 4 5) '(6) '(7 8))").toPyList()), 8)
        self.assertEqual(self.s.sh("""(string-append)"""), "")
        self.assertEqual(self.s.sh("""(string-append "ab" "cd")"""), "abcd")
        self.assertEqual(self.s.sh("""(string-append "ab" "cd" "ef")"""), "abcdef")
        self.assertEqual(self.s.sh("""(string-append "a" (number->string 1))"""), "a1")

    def testScope(self):
        s=Scm()
        self.assertEqual(s.sh("""1"""), 1)
        s.sh("""(define x 1)""")
        self.assertEqual(s.sh("""x"""), 1)
        s.sh("""(::begin (define (z x) x) (define (d x) x)(define y 1) y)""")
        self.assertEqual(s.sh("""(d 4)"""), 4)

    def testCtrl(self):
        self.assertEqual(s.sh("""(and (= 2 2) (> 2 1))"""), True)
        self.assertEqual(s.sh("""(and (= 2 2) (< 2 1))"""), False)
        self.assertEqual(s.sh("""(and 1 2 'c '(f g))"""), s.sh("""'(f g)"""))
        self.assertEqual(s.sh("""(and)"""), True)
        self.assertEqual(s.sh("""(or (= 2 2) (> 2 1))"""), True)
        self.assertEqual(s.sh("""(or (= 2 2) (< 2 1))"""), True)
        self.assertEqual(s.sh("""(or #f #f #f)"""), False)
        self.assertEqual(s.sh("""(or (member 'b '(a b c))(/ 3 0))"""), s.read("""(b c)"""))

    def testQuasiquote(self):
        self.assertEqual(s.sh("""`(a 1 ,(+ 1 1) ,@(list 1 2))"""), s.sh("""'(a 1 2 1 2)"""))
        self.assertEqual(s.sh("""((lambda ()(define (f x) (+ x 1))`(1 ,(f 1))))"""), s.sh("""'(1 2)"""))
        #self.assertEqual(s.sh("""(do ((i 1 (+ i 1))(s 0 (+ s i)))((> i 100)s))"""), s.sh("""5050"""))
        
    def testLet(self):
        self.assertEqual(s.sh("""(let* () 1 2 3)"""), 3)
        self.assertEqual(s.sh("""(let* ((a 3)) a)"""), 3)
        self.assertEqual(s.sh("""(let ((a 1)(b 2)) (+ a b))"""), 3)
        self.assertEqual(s.sh("""(let* ((a 1)(b a)) (+ a b b))"""), 3)
        self.assertEqual(s.sh("""(let ((x 2) (y 3))
                                  (let* ((x 7)
                                         (z (+ x y)))
                                    (* z x)))"""), 70)
        self.assertEqual(s.sh("""(letrec ((even?
                                      (lambda (n)
                                        (if (zero? n)
                                            #t
                                            (odd? (- n 1)))))
                                     (odd?
                                      (lambda (n)
                                        (if (zero? n)
                                            #f
                                            (even? (- n 1))))))
                              (even? 88))"""), True)
        self.assertEqual(s.sh("""(let ((a 1)(b 2)) (let* ((b a)(a b)) (= a b)))"""), True)

    def testChar(self):
        self.assertEqual(s.sh(r"(<= (char->integer #\a)(char->integer #\b))"), True)

    def testType2(self):
        self.assertTrue(self.s.sh("(pair? (quote (+ 1 2)))"))
        self.assertTrue(self.s.sh("(symbol? 'abc"))
        self.assertTrue(self.s.sh("(pair? (quote (+ 1 2)))"))
        self.assertTrue(self.s.sh("(pair? (quote (+ 1 2)))"))
        self.assertTrue(self.s.sh("(pair? (quote (+ 1 2)))"))
        self.assertTrue(self.s.sh("(pair? (quote (+ 1 2)))"))

    def testFix(self):
        self.assertEqual(self.s.sh("(- 1)"), -1)
        self.assertEqual(self.s.sh("(- 1 2)"), -1)
        self.assertEqual(self.s.sh("(/ 2 1)"), 2)
        self.assertEqual(self.s.sh("(not '())"), False)
        self.assertEqual(self.s.sh("(if 0 2 3)"), 2)
        self.assertTrue(self.s.sh("'a;a"),self.s.sh("'a"))
        self.assertTrue(self.s.sh(r"(char? #\SPaCE)"))

    def testFix2(self):
        self.assertEqual(self.s.sh("(let()1)"), 1)
        self.assertEqual(self.s.sh("((lambda () #(1)))"), self.s.sh(r"#(1)"))
        self.assertEqual(self.s.sh("(length '(1 2))"), 2)
        self.assertEqual(self.s.sh("(length '())"), 0)
    def testVector(self):
        self.assertEqual(self.s.sh(r"#(1)"),self.s.sh("(vector 1)"))
        self.assertEqual(self.s.sh(r"#(1 2)"),self.s.sh("(vector 1 2)"))
        self.assertEqual(self.s.sh(r"#(1 2 3)"),self.s.sh("(vector 1 2 3)"))
        self.assertEqual(self.s.sh(r"#()"),self.s.sh("(vector)"))
        self.assertEqual(self.s.sh(r"(map + '(1 2 3) '(4 5 6))"),self.s.sh("'(5 7 9)"))
        self.assertEqual(self.s.sh(r"(apply + 1 2 '(3 4)) "),10)
        
    def testOutside(self):
        self.s.load("test.scm",self.s.env())

    
        
        
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#define-apply
s = Scm()
r = s.repl
l = s.load
print s.sh(r"""1""")


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(200)
    #sys.setrecursionlimit(2**16-1)
    unittest.main()
