from part2 import *
import os
#print "####part2################"
class TypErr(Exception):
    pass
def pprint(sexp):
    return sexp
def load(filename,env):
    with open(filename) as f:#path.file
        return Scm.eval(Scm.read("(begin %s)"%f.read()),topenvrn)      
class Scm:
    def __init__(self,toplevel=None):
        toplevel=toplevel if toplevel else topenvrn
        self._env = toplevel.extend()
    def sh(self,code):
        return eval9(read(code)[0],self._env)
    @staticmethod    
    def load(filename,env):
        with open(os.path.abspath(filename)) as f:
            return Scm.eval(Scm.read("(begin %s)"%f.read()),topenvrn)  
    def env(self):
        return self._env
    def repl(self):
        while True:
            try:
                print self.sh(raw_input('scm> '))
            except Exception as e:
                print e
    @staticmethod
    def read(sexp):
        return read(sexp)[0]
    @staticmethod
    def eval(sexp,env):
        return eval9(sexp,env)
    @staticmethod
    def nilEnv(sexp,env):
        return Env()

def block(f):
    return f()
@block
def globalMacro():
    def defmacro(code):#not use outside,dut to scope
        sexp = Scm.read(code)
        assert sexp.car=='defmarco'
        name = sexp.cdr.car
        marco_rule = cons('lambda',sexp.cdr.cdr)
        def expend(sexp):
            trans = Scm.eval(marco_rule,topenvrn)#here?
            #print topenvrn.var.keys()
            #print 'list' in topenvrn.var.keys()
            #print sexp
            expended_code = trans.apply(sexp.cdr)
            #print expended_code if pairp(expended_code) and expended_code.car=='cons' else None
            return buildExp9(expended_code)
        topmacro[name] = expend
    def loadMacro(filename):
        with open(os.path.abspath(filename)) as f:
            code = f.read()
            #print "file>",code
            start = 0
            while 1:
                t,end = peekSexp(code,start)
                if end==-1:
                    break
                defmacro(code[start:end])
                start = end        
    with open(os.path.abspath("initsyx.scm")) as f:
        code = f.read()
        #print "file>",code
        start = 0
        while 1:
            t,end = peekSexp(code,start)
            if end==-1:
                break
            defmacro(code[start:end])
            start = end
    defmacro("""(defmarco define lst
                 (if (pair? (car lst))
                     (cons '::define (cons (car (car lst)) (cons (cons 'lambda (cons (cdr (car lst)) (cdr lst))) '())))
                     (cons '::define lst))))""")
    #defvar
    defmacro("""(defmarco begin lst
                    (cons '::begin lst))""")
    #defmacro(open("quasiquote.scm").read())
    loadMacro("quasiquote.scm")
    loadMacro("initsyn2.scm")
    return defmacro
defmacro = globalMacro
@block
def _():

    def check(ture):
        if not ture:
            raise Err()
        return True
    #topenvrn = Env()
    def defun(name,env=None):#this one is better
            env = env if env else topenvrn
            return lambda f:env.define(Sym(name),Prc(f))
    def define(name,value,env=None):
            env = env if env else topenvrn
            return env.define(Sym(name),value)
    def bindPyFun(name,func,env=None):
	    env = env if env else topenvrn
	    return env.define(name,Prc(lambda arg:apply(func,arg.toPyList())))
    def chanp(pred):
        def _(*lst):
            assert len(lst)>=2
            a = lst[0]
            for b in lst[1:]:
                if not pred(a,b):
                    return False
                a = b
            return True
        return _
    def chanpp(pred):#this one is better than chanp
        def _(pair):
            a,b = pair
            while 1:
                b,c = b
                if not pred(a,b):
                    return False
                if nullp(c):
                    return True
            raise Exception()
        return _
    
    bindFun = bindPyFun

    @block
    def base():
            @defun("display")
            def _(arg):
                    check(pairp(arg))
                    print arg.car
            @defun("newline")
            def _(arg):
                    print ;
            @defun("error")
            def _(arg):
                    raise Err("ERR ",arg.car)
            bindPyFun("null?",nullp)
            bindPyFun("procedure?",procedurep)
            define("apply",BlkApp9())

    @block
    def pair():
            bindPyFun("pair?",pairp)
            bindPyFun("cons",cons)
            bindPyFun("car",car)
            bindPyFun("cdr",cdr)

    @block
    def equal():
            @defun("eq?")
            @chanpp
            def _(x,y):
                    return (x is y) or (isa(x,str) and isa(y,str) and x==y)#use 'is' later
            @defun("eqv?")
            @chanpp
            def _(x,y):
                    return (not isa(x,tuple)) and (not isa(x,list)) and x==y#use 'is' for pair later
            @defun("equal?")
            @chanpp
            def _(x,y):
                    return x==y

        
    @block
    def math():
        define("+nan.0",float('nan'))
        bindPyFun("number?",numberp)
        define("+",PyFun(lambda *lst:reduce(lambda x,y:x+y,lst,0)))
        define("-",PyFun(lambda *lst:reduce(lambda x,y:x-y,lst,)))
        define("*",PyFun(lambda *lst:reduce(lambda x,y:x*y,lst,1)))
        define("/",PyFun(lambda *lst:reduce(lambda x,y:x/y,lst)))
        bindPyFun("=",chanp(lambda a,b:a==b))
        bindPyFun(">",chanp(lambda a,b:a>b))
        bindPyFun("<",chanp(lambda a,b:a<b))
        bindPyFun(">=",chanp(lambda a,b:a>=b))
        bindPyFun("<=",chanp(lambda a,b:a<=b))
        bindPyFun("integer?",lambda x:x%1==0)
##        @defun("<")
##        def _(x):
##            return x.car<x.cdr.car
##        @defun(">")
##        def _(x):
##            return x.car>x.cdr.car
##        @defun("=")
##        def _(x):
##            check(numberp(x.car))
##            check(numberp(x.cdr.car))
##            return x.car==x.cdr.car

    @block
    def math2():
        import math
        dct={
            'abs':abs,
            'quotient':lambda a,b:int(a / b),
            'remainder':lambda a,b:a-(b*int(a/b)),
            'modulo':lambda a,b:a % b,
            'floor':math.floor,
            'ceiling':math.ceil,
            'truncate':math.trunc,
            'round':round,
            'exp':math.exp,
            'log':math.log,
            'sin':math.sin,
            'cos':math.cos,
            'tan':math.tan,
            'asin':math.asin,
            'acos':math.acos,
            'atan':math.atan,
            'sqrt':math.sqrt,
            }
        for k,v in dct.items():
            bindPyFun(k,v)

    @block
    def logic():
        define("not",Prc(lambda arg:not arg.car))
##        define("#t",True)
##        define("#f",False)#use lex later

    
    @block
    def init():
        Scm.load("initlib.scm",topenvrn)     

    @block
    def string():
        define("string?",Prc(lambda arg:isa(arg.car,str) and not isa(arg.car,Sym)))
        define("string-append",PyFun(lambda *lst:reduce(lambda x,y:check(isa(x,str)) and check(isa(y,str)) and x+y,lst,'')))    
##            @defun("::string-append",topenvrn)
##            def _(x):
##                    check(isa(x.car,str))
##                    check(isa(x.cdr.car,str))
##                    return x.car+x.cdr.car
##            Scm.eval(Scm.read("""(define (string-append . x) (fold-left ::string-append "" x))"""),topenvrn)
    
    @block
    def typeToType():
            @defun("number->string",topenvrn)
            def _(x):
                    check(numberp(x.car))
                    return str(x.car)
    @block
    def vector():
        define("vector",Prc(lambda arg:arg.toPyList() if arg else []))
    
    @block
    def morelib():
        bindPyFun("list?",listp)
        #Scm.load("libtinyscheme.scm",topenvrn)

@block
def topExtend():
	pass
#topenvrn.define()
#print Scm().sh("1")
##print eval9(read("""((lambda ()
##     (define f (lambda (x) (display "IIIIIIIIIIIIIIIIIIIIIIIIIII") (+ x 1)))
##     (display "LLLLLLLLLLLLLLLLLL")
##     f
##    ))""")[0],toplevel.extend()).apply(cons(1,nil))
##print eval(cons(eval9(read("""
##((lambda ()
##     (define f (lambda () "III"))
##     f
##))
##""")[0],toplevel.extend()),nil),toplevel.extend())
####print eval9(read("""((lambda ()
##    (define (f x)(+ x 1))
##    (f 3)
##    ))""")[0],toplevel.extend()).apply(cons(1,nil))
