from part2 import Scm
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
        pass
    
    def testTodo(self):
        print self.s.sh("(lambda (x) (+ x 1))")
        print self.s.sh("((lambda ()(define f (lambda (x) (+ x 1)))f))")
        print self.s.sh("call/cc")
        
        
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
from part2 import eval9
s = Scm()
print s.sh("((lambda x (+ (car x) (car (cdr x)))) 1 2)")
if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(500)
    unittest.main()
