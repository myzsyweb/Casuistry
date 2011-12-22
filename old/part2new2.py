from cse2 import *
a=Env()
s=Sym
for i in range(10):
    a.define(s("int"+str(i)),i)
print a
for i in range(10):
    a.define(s("fix"+str(i)),-i)
print a
b=a.extend()
for i in range(5):
    b.define(s("fix"+str(i)),i)
print b
b.freezeIt()
#print b.offset(s('int2'))
#print b.offset(s('int4'))
print b.lookupByName(s('int9'))
print b.lookupByOffset(b.offset(s('fix2')))
print b.lookupByOffset([3])
c = b.extendByOffset(varnum=3)
print c,c.varnum
c.defineByOffset([1],3)
print c.lookupByOffset([1]),c.lookupByOffset([2])
d = b.extendByOffset(cons(s('hello'),None),cons('world',None),varnum=3)
print d.lookupByOffset([1])
print d.varnum
print b.lookupByName(s('fix3'))
#print b.lookup(s('fix3'))
print b.lookupByOffset(b.offset(s('fix3')))
d.defineByOffset([1],'whole')
print d.lookupByOffset([1])
feature_local=True#####
def sh(s):
    return eval9(read(s)[0])
print eval9(read('1')[0])
print eval9(read('(::define n 1)')[0])
print buildExp10(read('(::define n 1)')[0],Env())
print sh('(lambda x x)')
print sh('(::define f (lambda x x))')
print sh('(f 1)')
print sh('((lambda x x) 1 2 3)')
print sh('((lambda (f) (f 4)) (lambda (x) x))')
print sh('((lambda (f) ((f) 4)) (lambda () (lambda (x) x)))')
#from main import *
#Scm().repl()
##import csp
##s=csp.sh
##s('(::define dd 1)')
##s('dd')
##s('(define df 1)')
e=Env()
e.define(s('v'),1)
print e.lookup(s('v'))
e.freezeIt()
print e.lookup(s('v'))
v=e.extend()
print v.lookup(s('v'))
v.define(s('v'),2)
print v.lookup(s('v'))
v.freezeIt()
print v.lookup(s('v'))
from __init__ import *
sl = Scm().sh
#topenvrn.freezeIt()
print sl('((lambda () (define a 1) (+ a 1)))')
#topenvrn.freezeIt()#
sl('(+ 1 1)')
sl('((lambda (+) (+ 1 1))+)')
sl('((lambda () (+ 1 1)))')
#print sl('((lambda () (define a 1) (+ a 1)))')
def fastload(filename):
    e=topenvrn.extend()
    e.freezeIt()
    code="((lambda ()%s))"%(open(filename).read())
    print eval9(read(code)[0],e)
import sys
sys.setrecursionlimit(2**15-1)
from timeit import Timer
t = Timer("fastload('testcalc24.scm')", "from __main__ import fastload")
print t.timeit(1)
topenvrn.freezeIt()
t = Timer("fastload('testcalc24.scm')", "from __main__ import fastload")
print t.timeit(1)
#fastload('testcalc24.scm')
