from part3 import Scm
import unittest
class Test(unittest.TestCase):
    def setUp(self):
        self.s = Scm()
    def testBase(self):
        self.assertEqual(self.s.sh("1"), 1)
        self.assertEqual(self.s.sh("(+ 1 1)"), 2)
        self.assertEqual(self.s.sh("((lambda (x) (+ x 1)) 7 )"), 8)
        self.assertEqual(self.s.sh("(if (> 1 2) 3 4)"), 4)
        self.assertEqual(self.s.sh("((lambda () (define x 1) x))"), 1)
        self.assertEqual(self.s.sh("((lambda (p) (p 1))(lambda (x) (+ x 1)))"), 2)
        self.assertEqual(self.s.sh("""((lambda x (+ (car x) (car (cdr x)))) 1 2)"""), 3)
        
    def testRead(self):
        pass
    
    def testType(self):
        self.assertTrue(self.s.sh("(pair? (quote (+ 1 2)))"))
        
    def testOther(self):
        self.assertEqual((self.s.sh("(lambda (x) (+ x 1))"))(1), 2)
    
    def testCont(self):
        self.assertEqual(self.s.sh("""(call/cc (lambda (c) (display "show") (c 1) (display "hide") 2))"""), 1)
        
    def testTailCall(self):
        print self.s.sh("""((lambda ()(define f (lambda (n s) (if (< n 1) s (f (- n 1) (* n s)))))(f 1000 1)))""")
        
    def testMarco(self):
        self.assertEqual(self.s.sh("""((lambda ()(define (f x) (+ x 1))(f 4)))"""), 5)
        self.assertEqual(self.s.sh("""(begin (display 1) (display 2) 3)"""), 3)
        self.assertEqual(self.s.sh("""(let loop ((x 10))(if (< x 0) 0 (+ x (loop (- x 1)))))"""), 55)
        self.assertEqual(self.s.sh("""(cond((= 1 2) 3)((= 4 5) 6)(else 7))"""), 7)
        self.assertEqual(self.s.sh("""(case (+ 1 1)((1) 1)((2) 2))"""), 2)
        
    def testTodo(self):
        print self.s.sh("(lambda (x) (+ x 1))")
        print self.s.sh("((lambda ()(define f (lambda (x) (+ x 1)))f))")
        print self.s.sh("call/cc")
        
        
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#define-apply
s = Scm()
r = s.repl
print s.sh("1")
print s.sh("""(define x 1)""")
print s.sh("""x""")
print s.sh("""(::begin (define (z x) x) (define (d x) x)(define y 1) y)""")
print s.sh("""(d 4)""")
#print s.sh("""(define (z x) x)""")
if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(500)
    unittest.main()
