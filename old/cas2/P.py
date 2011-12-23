from T import *
#from cse2 import *
#splist to two file
import os
class PyFun(Prc):
    def __init__(self,func):
        self.func = func
    def __call__(self,*arg):
        return self.func(*arg)
    def apply(self,arg):
        assert pairp(arg) or nullp(arg) ,arg
        return apply(self.func,(arg.toPyList() if arg else []))
#print "####part2################"
class TypErr(Exception):
    pass
##def pprint(sexp):
##    return sexp
##def load(filename,env):
##    with open(filename) as f:#path.file
##        return Scm.eval(Scm.read("(begin %s)"%f.read()),topenvrn)

def installMacro(add):
    pass
##class Scm:
##    def __init__(self,toplevel=None):
##        toplevel=toplevel if toplevel else topenvrn
##        self._env = toplevel.extend()
##    def sh(self,code):
##        return eval9(read("(::begin %s)"%code)[0],self._env)
##    @staticmethod    
##    def load(filename,env):
##        with open(filename) as f:
##            return Scm.eval(Scm.read("(::begin %s)"%f.read()),env)#?  
##    def env(self):
##        return self._env
##    def repl(self):
##        while True:
##            try:
##                print self.sh(raw_input('scm> '))
##            except Exception as e:
##                print e
##    @staticmethod
##    def read(sexp):
##        return read(sexp)[0]
##    @staticmethod
##    def eval(sexp,env):
##        return eval9(sexp,env)
##    @staticmethod
##    def nilEnv(sexp,env):
##        return Env()

def block(f):
    return f()
#waste=[]
##@block
##def globalMacro():
##    def defmacro(code):#not use outside,dut to scope
##        sexp = Scm.read(code)
##        assert sexp.car==Sym('defmarco')#shoud defmcro
##        name = sexp.cdr.car
##        marco_rule = cons(Sym('lambda'),sexp.cdr.cdr)
##        def expend(sexp,cenv):
##            trans = Scm.eval(marco_rule,topenvrn)#here?
##            #print topenvrn.var.keys()
##            #print 'list' in topenvrn.var.keys()
##            #print sexp.car
####            if sexp in waste:
####                #raise Exception(sexp)
####                print sexp
####            else:
####                waste.append(sexp)
##            expended_code = trans.apply(sexp.cdr)
##            #print expended_code if pairp(expended_code) and expended_code.car=='cons' else None
##            #print expended_code
##            
##            #return buildExp9(expended_code)
##            return buildExp10(expended_code,cenv)#move to part2 and use cenv
##            #return buildExp10(expended_code,topenvrn.extend())
##        topmacro[name] = expend
##    def loadMacro(filename):
##        with open(os.path.abspath(filename)) as f:
##            code = f.read()
##            #print "file>",code
##            start = 0
##            while 1:
##                t,end = peekSexp(code,start)
##                if end==-1:
##                    break
##                defmacro(code[start:end])
##                start = end 
##    loadMacro("initsyx.scm")
##    defmacro("""(defmarco define lst
##                 (if (pair? (car lst))
##                     (cons '::define (cons (car (car lst)) (cons (cons 'lambda (cons (cdr (car lst)) (cdr lst))) '())))
##                     (cons '::define lst))))""")
##    #defvar
##    defmacro("""(defmarco begin lst
##                    (cons '::begin lst))""")
##    #defmacro(open("quasiquote.scm").read())
##    loadMacro("quasiquote.scm")
##    loadMacro("do.scm")
##    loadMacro("initsyn2.scm")
##    return defmacro
#defmacro = globalMacro
#@block
def makePrim(add,topenvrn,Scm):
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
                return env.define(Sym(name),Prc(lambda arg:apply(func,arg.toPyList())))
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
                a,b = pair.car,pair.cdr
                while 1:
                    b,c = b.car,b.cdr
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
                #define("apply",BlkApp9())#move later

        @block
        def pair():
                bindPyFun("pair?",pairp)
                bindPyFun("cons",cons)
                bindPyFun("car",car)
                bindPyFun("cdr",cdr)
##                bindPyFun("set-car!",mset_car)
##                bindPyFun("set-cdr!",mset_cdr)
                @defun("list")
                def _(arg):
                    return arg

        @block
        def equals():
            bindPyFun("eq?",chanp(eq))
            bindPyFun("eqv?",chanp(eqv))
            bindPyFun("equal?",chanp(equal))
    ##            @defun("eq?")
    ##            @chanpp
    ##            def _(x,y):
    ##                    return (x is y) or (isa(x,Sym) and isa(y,Sym) and x==y)#use 'is' later
    ##            @defun("eqv?")
    ##            @chanpp
    ##            def _(x,y):
    ##                    return (not isa(x,tuple)) and (not isa(x,list)) and x==y#use 'is' for pair later
    ##            @defun("equal?")
    ##            @chanpp
    ##            def _(x,y):
    ##                    return x==y

            
        @block
        def math():
            from numbers import Complex,Real,Rational
            define("+nan.0",float('nan'))
            bindPyFun("number?",numberp)
            define("+",PyFun(lambda *lst:reduce(lambda x,y:x+y,lst,0)))
            define("-",PyFun(lambda *lst:reduce(lambda x,y:x-y,lst) if len(lst)>1 else -lst[0]))
            define("*",PyFun(lambda *lst:reduce(lambda x,y:x*y,lst,1)))
            define("/",PyFun(lambda *lst:reduce(lambda x,y:x/y,lst) if len(lst)>1 else 1/lst[0]   ))
            bindPyFun("=",chanp(lambda a,b:a==b))
            bindPyFun(">",chanp(lambda a,b:a>b))
            bindPyFun("<",chanp(lambda a,b:a<b))
            bindPyFun(">=",chanp(lambda a,b:a>=b))
            bindPyFun("<=",chanp(lambda a,b:a<=b))
            bindPyFun("integer?",lambda x:x%1==0)#can be inex!
            bindPyFun("complex?",lambda x:isa(x,Complex))
            bindPyFun("real?",lambda x:isa(x,Real))
            bindPyFun("rational?",lambda x:isa(x,Rational))
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
            #from math import exp,log
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
                'expt':pow,#use builtin not math's
                }
            for k,v in dct.items():
                bindPyFun(k,v)

        @block
        def logic():
            define("not",Prc(lambda arg:not truep(arg.car)))
            bindPyFun("boolean?",booleanp)
    ##        define("#t",True)
    ##        define("#f",False)#use lex later

        
        @block
        def init():
            pass
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
        def typeToType():#remove later
                @defun("number->string",topenvrn)
                def _(x):
                        check(numberp(x.car))
                        return str(x.car)
                @defun("char->integer",topenvrn)
                def _(x):
                        check(charp(x.car))
                        return ord(x.car)
                @defun("integer->char",topenvrn)
                def _(x):
                        #check(charp(x.car))
                        return chr(int(x.car))                
                    
        @block
        def vector():
            define("vector",Prc(lambda arg:Vec(arg.toPyList() if arg else [])))
            bindPyFun("vector?",vectorp)
            bindPyFun("make-vector",lambda k,f=None:[f]*int(k))
            bindPyFun("vector-ref",lambda v,k:v[int(k)])
        
        @block
        def morelib():
            bindPyFun("list?",listp)
            bindPyFun("symbol?",symbolp)
            bindPyFun("char?",charp)
            #Scm.load("libtinyscheme.scm",topenvrn)#move to singlepart later
    assert not topenvrn.freeze
#makePrim(lambda k,v:topenvrn.define(k,v))
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
    
##def sh(s):
##    return eval9(read(s)[0])
    
#assert not topenvrn.freeze
#topenvrn.freezeIt()
"""


"""
