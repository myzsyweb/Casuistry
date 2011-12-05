from part4 import peekSexp,Scm,topmacro,pp
import sys
sys.setrecursionlimit(2**15-1)
def read(text):
    return peekSexp(text)[0]
#code = open("qqt.scm").read()
#print code
#print read(code)
s = Scm()
#print s.sh(code)
##print read("(apply quasiquwteex (cdr '(quasiquwte ((unquwte +) 1 (unquwte a)))))")
##print s.sh("(+ 1 2 3)")
##print s.sh("(apply (lambda x x) (list 1 2 3))")
##print s.sh("(apply quasiquwteex '(((unquwte +) 1 (unquwte a))))")
##print s.sh("(apply quasiquwteex (cdr '(quasiquwte ((unquwte +) 1 (unquwte a)))))")
print (s.load("testmacro.scm",s.env()))
#print topmacro["quasiquote"](s.read("(1 2)"))
#print s.sh("`(a 2 3)")
