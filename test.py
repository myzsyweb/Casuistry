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
        pass
        #self.assertEqual(s.sh("""`(a 1 ,(+ 1 1) ,@(list 1 2))"""), s.read("""'(a 1 2 1 2)"""))

        
    def testOutside(self):
        self.s.load("test.scm",self.s.env())

    
        
        
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#define-apply
s = Scm()
r = s.repl
l = s.load
print s.sh("1")


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(200)
    unittest.main()
