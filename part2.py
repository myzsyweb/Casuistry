#tail-call
from part1 import *
import sys
sys.setrecursionlimit(100)
def pyListToSexp(lst):
    return reduce(lambda s,i:cons(i,s),reversed(lst),nil)
def pyListToPair(lst):
    return reduce(lambda s,i:cons(i,s),reversed(lst),nil)
def id(self):
    return self

##class Lambda:
##    def __init__(self,func):
##        self.func=func
##    def __call__(self,*arg,**kw):
##        return self.func(*arg,**kw)
class IdT:
    def __repr__(self):
        return 'Type %s %s'%(self.__class__,tuple.__repr__(self))    
class Tuk(tuple):
    def __repr__(self):
        return 'Type %s %s'%(self.__class__,tuple.__repr__(self))
def tuk(cont,arg):
    assert isa(arg,tuple)
    return Tuk((cont,arg))
def cnt(self):
    return self
def runtail(f,*x):
    while f:
#        try:
            #print "runtail>>>",x
        f, x = f(*x)
#        except Exception as e:
#            print "runtail>",e,f.__class__,x
#            raise Exception(e)
    return x   
def tukrun(tuk):
    assert isa(tuk,Tuk)
    return runtail(tuk[0],*tuk[1]) 
##class DelayCall:
##    def __init__(self,func,*arg,**kw):
##        pass
##class Cont:
##    pass
class Apy:
    pass
class ApyC:
    pass
class ApyCT:
    pass
class PyFunc(Prc):
    def __init__(self,func):
        self.func = func
    def __call__(self,*arg):
        return self.func(*arg)
    def apply(self,arg):
        assert pairp(arg) or nullp(arg)
        return self.func(sexpToPyList(arg))
class BlkLmd9(Prc):
    def __init__(self,arg,blk,env):
        self.arg = arg
        self.bdy = blk#getStmt()
        self.env = env
    def __repr__(self):
        return 'LAMBDA '+object.__repr__(self)
    def __call__(self,*arg):
        print ">>>",pyListToSexp(arg)
        return self.apply(pyListToSexp(arg))
    def apply(self,arg): 
        rt = self.env.extend(self.arg,arg)
        def quote(arg):
            return cons('quote',cons(arg,nil))
        return eval9(cons(self,arg.map(quote)),rt)
    def apply9(self,arg,cont):
        rt = self.env.extend(self.arg,arg)
        #print "????",self.bdy(rt,cont)
        return self.bdy(rt,cont)
class BlkCont9(BlkLmd9):
    def __init__(self,env,c):
        self.env = env
        self.bdy = c
    def __repr__(self):
        return "LAMBDA continuation"
    def apply(self,arg):
        BlkLmd9.apply(self,arg)
        raise Exception()
    def apply2(self,arg,cont):
        return self.bdy(arg.car)
    def apply9(self,arg,cont):
        return self.bdy(arg.car)
class BlkCwcc9(BlkLmd9):
    def __init__(self,env):
        self.env = env
    def __repr__(self):
        return "LAMBDA 'call/cc'"
    def apply(self,arg):
        BlkLmd9.apply(self,arg)
        raise Exception()
    def apply9(self,arg,cont):
        if not isa(arg.car,BlkLmd9):
            raise Exception()
        return arg.car.apply9(cons(BlkCont9(self.env,cont),nil),cont)

##def macroExpend(sexp):
##    pass

##class SymDct(dict):
##    pass
topmacro = {}
topenvrn = Env()
def buildExp9(sexp):
    raw_define = Sym('::define')
    def form(sexp):
        assert pairp(sexp)
        op = car(sexp)
        if op==Sym('if'):
            test = build(sexp.cdr.car)
            then = build(sexp.cdr.cdr.car)
            fail = build(sexp.cdr.cdr.cdr.car)
            return lambda env,c:tuk(test,(env,lambda v:then(env,c)if v else fail(env,c)))
        elif op==Sym('lambda'):
            arg = sexp.cdr.car
            bodys = sexp.cdr.cdr.map(build)#to one blk
            #bodyq = lambda env,c:tuk(reduce,(lambda cont,blk:(lambda v:blk(env,cont)),reversed(bodys.toPyList()),c))
            def get_seqs(sexpbodys):
                def seq(x,y):
                    return lambda env,c:tuk(x,(env,lambda v:y(env,c)))
                def loop(h,t):
                    if nullp(t):
                        return h
                    else:
                        return loop(seq(h,t.car),t.cdr)
                bodys = sexpbodys.map(build)
                return loop(bodys.car,bodys.cdr)
            return lambda env,c:tuk(c,(BlkLmd9(arg, get_seqs(sexp.cdr.cdr) ,env),))
        elif op==raw_define:
            name = sexp.cdr.car
            val = build(sexp.cdr.cdr.car)
            return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))
        elif op==Sym('quote'):
            val = sexp.cdr.car
            return lambda env,c:tuk(c,(val,))
        raise Exception()    
    def build(sexp):
        if pairp(sexp):
            if car(sexp) in [Sym('if'),Sym('lambda'),Sym('quote'),raw_define]:
                return form(sexp)
            if car(sexp) in topmacro:
                #raise "define"
                return topmacro[car(sexp)](sexp)
            op = build(car(sexp))
            arg = sexp.cdr.map(build) if sexp.cdr else None
            def get_args(arg,env,cont):
                if nullp(arg):
                    return cont(nil)
                else:
                    return car(arg)(env,lambda v1:get_args(arg.cdr,env,lambda v2:cont(cons(v1,v2))))
            def app(obj,arg,cont):
##                if isa(obj,BlkLmd4):
##                    raise Exception() 
##                    return obj.apply2(arg,cont)
                if isa(obj,BlkLmd9):
                    return obj.apply9(arg,cont)
                else:
                    return cont(obj.apply(arg))  
            return lambda env,c:tuk(op,(env,lambda v1:get_args(arg,env,lambda v2:app(v1,v2,c))))
        elif sexp==Sym('call/cc'):
            return lambda env,c:tuk(c,(BlkCwcc9(env),))
        elif isa(sexp,Sym):
            return lambda env,c:tuk(c,(env.lookup(sexp),))
        else:
            return lambda env,c:tuk(c,(sexp,))
    return build(sexp)
def eval9(sexp,env):
    t=[0]
    def ret(val):
        t[0] = val
        return None,(val,)
    #print "eval9]",buildExp9(sexp)(env,ret)
    tukrun(buildExp9(sexp)(env,ret))
    return t[0]

##toplevel9 = None
##def inEnv():
##    return toplevel
print "####part2################"
class TypErr(Exception):
    pass
def peekSexp(code):
    return read(code)
def read1(code):
    return read(code)[0]
##class Typ:
##    @staticmethod
##    def pairp(obj):
##        return pairp(obj)
class Scm:
    def __init__(self,toplevel=None):
        toplevel=toplevel if toplevel else topenvrn
        self._env = toplevel.extend()
    def sh(self,code):
        return eval9(read(code)[0],self._env)
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
def defmacro(code):
    sexp = Scm.read(code)
    #print ">",Scm.read(code)
    assert sexp.car=='defmarco'
    name = sexp.cdr.car
    marco_rule = cons('lambda',sexp.cdr.cdr)
    trans = Scm.eval(marco_rule,Scm().env())
    def expend(sexp):
        expended_code = trans.apply(sexp.cdr)
        return buildExp9(expended_code)
    topmacro[name] = expend
defmacro("""(defmarco define lst
         (if (pair? (car lst))
             (list '::define (car (car lst)) (cons 'lambda (cons (cdar lst) (cdr lst))))
             (cons '::define lst)))""")
def block(f):
    return f()
@block
def _():
    def build(*arg,**kw):
            return lambda f:f(*arg,**kw)
    def bldr(f):
            return f()
    def genv():
            return topenvrn
    def check(ture):
            if not ture:
                    raise Exception()
    #topenvrn = Env()
    def defun(name,env):
            return lambda f:env.define(Sym(name),Prc(f))
    def bindPyFunc(env,name,proc):
            return env.define(name,Prc(lambda arg:apply(proc,arg.toPyList())))

    @build(topenvrn)
    def defineToplevel(env):
            @defun("display",env)
            def _(arg):
                    check(pairp(arg))
                    print arg.car
                    return None
            @defun("newline",env)
            def _(arg):
                    print ;
                    return None
            @defun("apply",env)
            def _(arg):
                    check(isa(arg.car,Prc))
                    return arg.car.apply(arg.cdr.car)
            @defun("cons",env)
            def _(arg):
                    check(pairp(arg))
                    check(pairp(arg.cdr))
                    check(nullp(arg.cdr.cdr))
                    return Par.cons(arg.car,arg.cdr.car)
            @defun("car",env)
            def _(arg):
                    check(pairp(arg))
                    check(pairp(arg.car))
                    check(nullp(arg.cdr))
                    return arg.car.car
            @defun("cdr",env)
            def _(arg):
                    return arg.car.cdr
            @defun("<",env)
            def _(x):
                    return x.car<x.cdr.car
            @defun(">",env)
            def _(x):
                    return x.car>x.cdr.car
            @defun("=",env)
            def _(x):
                    check(numberp(x.car))
                    check(numberp(x.cdr.car))
                    return x.car==x.cdr.car
            @defun("eq?",env)
            def _(x):
                    return x.car==x.cdr.car#use 'is' later
            @defun("eqv?",env)
            def _(x):
                    return x.car==x.cdr.car#use 'is' for pair later
            @defun("equal?",env)
            def _(x):
                    return x.car==x.cdr.car
            @defun("-",env)
            def _(x):
                    return x.car-x.cdr.car
    topenvrn.define("+",Prc(lambda arg:reduce(lambda x,y:x+y,arg.toPyList() if arg else [],0)))
    #topenvrn.define("-",Prc(lambda arg:reduce(lambda x,y:x-y,arg.toPyList())))
    topenvrn.define("*",Prc(lambda arg:reduce(lambda x,y:x*y,arg.toPyList()if arg else [],1)))
    topenvrn.define("/",Prc(lambda arg:reduce(lambda x,y:x/y,arg.toPyList())))
    topenvrn.define("pair?",Prc(lambda arg:pairp(arg.car)))
    #topenvrn.define("null?",Prc(lambda arg:nullp(arg.car)))
    bindPyFunc(topenvrn,"null?",nullp)
    bindPyFunc(topenvrn,"number?",numberp)
    #topenvrn.define("number?",Prc(lambda arg:numberp(arg.car)))
    #topenvrn.define("number?",Prc(lambda arg:numberp(arg.car)))
    topenvrn.define("not",Prc(lambda arg:not arg.car))
    topenvrn.define("list",Lmd(read('(lambda x x)')[0],topenvrn))
    topenvrn.define("cdar",Lmd(read('(lambda (x) (cdr (car x)))')[0],topenvrn))
    topenvrn.define("cadr",Lmd(read('(lambda (x) (car (cdr x)))')[0],topenvrn))
    topenvrn.define("#t",True)
    topenvrn.define("#f",False)#use lex later
##    Scm.eval(Scm.read("""
##    (define (fold-right p i x)
##      (if (null? x) i
##              (p (car x) (fold-right p i (cdr x)))))
##    """),topenvrn)
##    Scm.eval(Scm.read("""
##    (define (fold-left p i x)
##      (if (null? x) i
##              (fold-left p (p i (car x)) (cdr x))))
##    """),topenvrn)
##    Scm.eval(Scm.read("""(define (map f x) (fold-right (lambda (a b) (cons (f a) b)) '() x))""")[0],topenvrn)
##    Scm.eval(Scm.read("""
##    (define (append . x) 
##      (define (append a b)
##            (if (null? a) b
##                    (cons (car a) (append (cdr a) b))))
##      (fold-left append '() x))
##    """),topenvrn)
##    Scm.eval(Scm.read("""
##    (define (member obj lst)
##      (cond
##            ((null? lst) #f)
##            ((equal? obj (car lst)) lst)
##            (else (member  obj (cdr lst)))))
##    """)[0],topenvrn)
##    eval(read("""
##    (define (zero? n) (= n 0))
##    """)[0],topenvrn)
##    @bldr
##    def defineString():
##            @defun("::string-append",topenvrn)
##            def _(x):
##                    check(isa(x.car,str))
##                    check(isa(x.cdr.car,str))
##                    return x.car+x.cdr.car
##            eval(read("""(define (string-append . x) (fold-left ::string-append "" x))""")[0],topenvrn)
    @bldr
    def defineType():
            @defun("number->string",topenvrn)
            def _(x):
                    check(numberp(x.car))
                    return str(x.car)
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
