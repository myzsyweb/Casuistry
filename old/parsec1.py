#!python2.7
##############info#######################
"""
@auhor ee.zsy
@date Nov.25,2010
"""

#def parsec(string)
##s=seq("(",or(num,str),")")
#num=
#str=


##s=r'142.3.2"s\td\"fa"sd f'
##s=r"'sfdf ggg"
code="""
(define fac
  (lambda (x)
    (if (> x 0) 
        (* x (fac (- x 1)))
        1)))
(fac 5)
"""
def isa(obj,typ):
    return isinstance(obj,typ)
#######################lex##########################
import re
pattern = r'''
 (?P<lpr>\()
|(?P<rpr>\))
|(?P<qte>\')
|(?P<num>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)
|(?P<str>\"(\\.|[^"])*\")
|(?P<sym>[^ \)\(\t\n\r]+)
|(?P<wht>[ \t\n\r]+)
'''
token = re.compile(pattern,re.S|re.X)
def peekToken(text,start=0):
    regex = token.match(text,start)
    if regex:
        tag = [(k,v) for k,v in regex.groupdict().items() if v]
        return tag[0],regex.end()
    return None,None
##peekToken(code)
##def  tokenTest(code):
##    tmp = code
##    nxt = 0
##    while nxt is not None:
##        tag,nxt = peekToken(tmp,nxt)
##        print tag
##tokenTest(code)
#########################type####################
def cons(car,cdr):
    return (car,cdr)
def car(pair):
    return pair[0]
def cdr(pair):
    return pair[1]
def nullp(obj):
    return obj is None
def pairp(pair):
    return isinstance(pair,tuple) and len(pair)==2
def sexpToPyList(pair):
    pyList = []
    while not nullp(pair):
        pyList.append(car(pair))
        pair = cdr(pair)
    return pyList
class T:
    pass
class Par(tuple):
    @property
    def car(self):
        return self[0]
    @property
    def cdr(self):
        return self[1]
    @staticmethod
    def cons(car,cdr):
        return Par((car,cdr))
    def map(self,pred):
        return Par.cons(pred(self.car),self.cdr.map(pred) if self.cdr else None)
    def fold(self,pred):
        return 
    def toPyList(self):
        pair = self
        pyList = []
        while pair:
            pyList.append(pair.car)
            pair = pair.cdr
        return pyList        
class Sym(str):
    pass
class Str(str):
    pass
from fractions import Fraction 
class Num(Fraction):
    pass
class Bol:
    pass
class Env:
    def __init__(self,var=None,bas=None):
        self.bas = bas
        self.var = var or {}
    def __repr__(self):
        return str((self.var,self.bas))
    def define(self,sym,val):
        self.var[sym] = val;
    def lookup(self,sym):
        if sym in self.var:
            return self.var[sym]
        elif self.bas is not None:
            return self.bas.lookup(sym)
        else:
            raise Exception("I can't understand what '%s' means?"%sym)
    def extend(self,arg=None,val=None):
        #print "extend>",arg,val
        var = {}
        while not nullp(arg):
            var[car(arg)]=car(val)
            arg,val=map(cdr,(arg,val))
        #print "extend>",var
        return Env(var,self)
class Prc:
    def __init__(self,pred=None):
        self.pred = pred
    def apply(self,arg):
        if self.pred:
            return self.pred(arg)
        else:
            raise NotImplementedError
class Lmd(Prc):
    def __init__(self,lmd,env):
        self.lmd = lmd
        self.arg = lmd.cdr.car
        self.bdy = lmd.cdr.cdr#!!!
        self.env = env
    def __repr__(self):
        return str(self.lmd)
    def apply(self,arg):
        #print "body>",self.bdy
        rt = self.env.extend(self.arg,arg)#entend env here!!!
        return self.bdy.map(lambda x:eval(x,rt)).toPyList()[-1]
        #fold-left
        #return eval(self.bdy,self.env.extend(self.arg,arg))  
#########################yacc####################
class Reader:
    pass
class SyxErr(Exception):
    pass
def read(text):
    def sexp(s,pos):
        tag,end = peekToken(s,pos)
        if not tag:
            return "$",-1
        if tag[0]=='wht':
            return sexp(s,end)
        elif tag[0]=='sym':
            return Sym(tag[1]),end
        elif tag[0]=='num':
            return Num(tag[1]),end
        elif tag[0]=='str':
            return Str(tag[1]),end
        elif tag[0]=='qte':
            exp,end = sexp(s,end)
            if end==-1:
                return "syx err",-1
            return Par((Sym("quote"),exp)),end
        elif tag[0]=='lpr':
            exp,end = srst(s,end)
            if end==-1:
                return "syx err",-1
            return (exp),end
    def srst(s,pos):
        tag,end = peekToken(s,pos)
        if not tag:
            return "$",-1
        if tag[0]=='wht':
            return srst(s,end)        
        elif tag[0]=='rpr':
            return None,end
        else:
            exp,end = sexp(s,pos)
            if end==-1:
                return "syx err",-1
            exp2,end2 = srst(s,end)
            if end2==-1:
                return "syx err",-1        
            return Par((exp,exp2)),end2
    return sexp(text,0)
print read(code)
print read("(+ a b c)")
###################eval##########################
def form(sexp,env):
    assert pairp(sexp)
    op = car(sexp)
    if op==Sym('if'):
        test = eval(sexp.cdr.car,env)
        if test:
            return eval(sexp.cdr.cdr.car,env)
        else:
            return eval(sexp.cdr.cdr.cdr.car,env)
    elif op==Sym('lambda'):
        return Lmd(sexp,env)
    elif op==Sym('define'):
        env.define(sexp.cdr.car,eval(sexp.cdr.cdr.car,env))
        return None
    elif op==Sym('quote'):
        return sexp.cdr
    elif op==Sym('+'):#!!!remove later
        return sum(map(lambda x:eval(x,env),sexpToPyList(cdr(sexp))))
    elif op==Sym('apply'):
        raise NotImplementedError()
    raise Exception()
def eval(sexp,env):
    if pairp(sexp):
        if car(sexp) in [Sym('if'),Sym('lambda'),Sym('quote'),Sym('define')]:
            return form(sexp,env)     
        op = eval(car(sexp),env)
        if isa(op,Prc):
            return op.apply(sexp.cdr.map(lambda x:eval(x,env)) if sexp.cdr else None)
        else:
            raise Exception(type(sexp),sexp)
    elif isa(sexp,Sym):
        return env.lookup(sexp)
    else:
        return sexp
############################toplevel#####################
toplevel = Env()
def display(text):
    print text
toplevel.define("display",Prc(lambda arg:display(arg.car)))
toplevel.define("+",Prc(lambda arg:reduce(lambda x,y:x+y,arg.toPyList(),0)))
toplevel.define("-",Prc(lambda arg:reduce(lambda x,y:x-y,arg.toPyList())))
toplevel.define("*",Prc(lambda arg:reduce(lambda x,y:x*y,arg.toPyList(),1)))
toplevel.define("/",Prc(lambda arg:reduce(lambda x,y:x/y,arg.toPyList())))
toplevel.define(">",Prc(lambda arg:reduce(lambda x,y:x>y,arg.toPyList())))
toplevel.define("<",Prc(lambda arg:reduce(lambda x,y:x<y,arg.toPyList())))

#print read("((lambda x (apply + x)) 1 58)")[0]
#print eval(read("((lambda x (apply + x)) 1 58)")[0],Env())
#############conti###############
#######################repl#################
class Repl():
    pass
def repl():
    pass
##############test##########################
import unittest
class Test(unittest.TestCase):
    def test_env(self):
        a = Env()
        b = a.extend()
        a.define("a",1)
        self.assertTrue(b.lookup("a")==1)
        b.define("a",2)
        self.assertTrue(a.lookup("a")==1)
        self.assertTrue(b.lookup("a")==2)
    def test_read(self):
        self.assertEqual(len(read("(+ 1 4)")[0].toPyList()),3)
    def test_calc(self):
        self.assertEqual( eval(read("(+ 1 6)")[0],toplevel.extend()) ,7)
        self.assertTrue( isa(eval(read("(lambda (x) (+ x 1))")[0],toplevel.extend()),Prc))
        self.assertEqual(eval(read("(display 1)")[0],toplevel.extend()),None)
        self.assertEqual( eval(read("((lambda (x) (+ x 1)) 7 )")[0],toplevel.extend()) ,8)
        self.assertEqual( eval(read("((lambda (x y) (+ x y)) 1 9)")[0],toplevel.extend()) ,10)
        self.assertEqual( eval(read("((lambda () (define x 1) (+ x 2)))")[0],toplevel.extend()) ,3)
        self.assertEqual( eval(read("((lambda () (define x 1) (if (> 1 2) x (+ x 6))))")[0],toplevel.extend()) ,7)
    def test_frac(self):
        code = """
            ((lambda ()
                (define fac
                  (lambda (x)
                    (if (> x 0) 
                        (* x (fac (- x 1)))
                        1)))
                (fac 6)))
        """
        self.assertEqual(
            eval(read(code)[0],toplevel.extend()),720)  
if __name__ == '__main__':
    pass
    #repl()
    #unittest.main()
print read("(+ 1 8)")
print eval(read("""((lambda ()
(define fac
  (lambda (x)
    (if (> x 0) 
        (* x (fac (- x 1)))
        1)))
(fac 6)
))""")[0],toplevel.extend())
