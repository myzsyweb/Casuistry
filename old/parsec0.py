#def parsec(string)
##s=seq("(",or(num,str),")")
#num=
#str=
import re
from fractions import Fraction 
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
class Cons(tuple):
    def __init__(self,car,cdr):
        self.__init__((car,cdr))
    def car(self):
        return self[0]
    def cdr(self):
        return self[1]
class Sym(str):
    pass
class Str(str):
    pass
class Num(Fraction):
    pass
class Env:
    def __init__(self,var=None,bas=None):
        self.bas = bas
        self.var = var or {}
    def define(self,sym,val):
        self.var[sym] = val;
    def lookup(self,sym):
        if sym in self.var:
            return self.var[sym]
        elif self.bas is not None:
            return slef.bas.lookup(sym)
        else:
            raise Exception()
class Prc:
    def __init__(arg,bdy,env):
        self.arg=arg
        self.bdy=bdy
        self.env=env
    def apply(arg):
        eval(self.bdy,Env(base=self.env))
#########################yacc####################
class Ecp(Exception):
    pass
def read(text):
    def sexp(s,pos):
        tag,end = peekToken(s,pos)
        if not tag:
            return "$",-1
        if tag[0]=='wht':
            return sexp(s,end)
        elif tag[0]=='sym':
            return ("id",tag[1]),end
        elif tag[0]=='num':
            return Num(tag[1]),end
        elif tag[0]=='str':
            return Str(tag[1]),end
        elif tag[0]=='qte':
            exp,end = sexp(s,end)
            if end==-1:
                return "syx err",-1
            return (Sym("quote"),exp),end
        elif tag[0]=='lpr':
            exp,end = srst(s,end)
            if end==-1:
                return "syx err",-1
            return (exp),end
    def srst(s,pos):
        tag,end = peekToken(s,pos)
        if not tag:
            return "$",-1
        if tag[0]=='rpr':
            return None,end
        else:
            exp,end = sexp(s,pos)
            if end==-1:
                return "syx err",-1
            exp2,end2 = srst(s,end)
            if end==-1:
                return "syx err",-1        
            return (exp,exp2),end2
    return sexp(text,0)
print read(code)
print read("(+ a b c)")
###################eval##########################

def eval(sexp,env):
    if pairp(sexp):
        if car(sexp)==('id','if'):
            return "TODO:if"
        elif car(sexp)==('id','lambda'):
            print "lambda "
            return "TODO:lambda"
        elif car(sexp)==('id','define'):
            return "TODO:define"
        elif car(sexp)==('id','+'):
            return sum(sexpToPyList(cdr(sexp)))
        elif pairp(car(sexp)):
            if car(sexp)[0]=='id':
                pass
            else:
                op = eval(car(sexp),env)
                return "TODO:evalop"
            return "TODO:var"
        else:
            raise Exception()
    else:
        return sexp
    return "TODO"
toplevel = Env()
#toplevel.define("+","a")
print read("(+ 1 8)")
print sexpToPyList(read("(+ 1 4)")[0])
print eval(read("(+ 1 6)")[0],Env())
print eval(read("((lambda (x y) (+ x y)) 1 2)")[0],Env())
print read("((lambda x (apply + x)) 1 58)")[0]
print eval(read("((lambda x (apply + x)) 1 58)")[0],Env())
