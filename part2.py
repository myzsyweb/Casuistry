#tail-call
from parsec import *
import sys
sys.setrecursionlimit(100)
def pyListToSexp(lst):
    return reduce(lambda s,i:cons(i,s),reversed(lst),nil)
def pyListToPair(lst):
    return reduce(lambda s,i:cons(i,s),reversed(lst),nil)
def id(self):
    return self

class Lambda:
    def __init__(self,func):
        self.func=func
    def __call__(self,*arg,**kw):
        return self.func(*arg,**kw)
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
##        raise Exception()
        rt = self.env.extend(self.arg,arg)
##        t = ["err"]
##        def ret(val):
##            t[0] = val
##        print ">>>>>>>>>>>",tukrun(self.bdy(rt,ret))
        return eval9(cons(self,arg),rt)#!!
##    def apply2(self,arg,cont):
##        rt = self.env.extend(self.arg,arg)
##        return self.bdy(rt,cont)
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
def buildExp9(sexp):
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
        elif op==Sym('define'):
            name = sexp.cdr.car
            val = build(sexp.cdr.cdr.car)
            #return lambda env,c:tuk(id,c(val(env,lambda v:c(env.define(name,v)))))
            #return lambda env,c:tuk(c,("<define>",))
            return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))
            #return lambda env,c:tuk(c,(val(env,lambda v:c(env.define(name,v))),))
            #return lambda env,c:c(val(env,lambda v:c(env.define(name,v))))
        elif op==Sym('quote'):
            val = sexp.cdr.car
            return lambda env,c:tuk(c,(val,))
        raise Exception()
    def build(sexp):
        if pairp(sexp):
            if car(sexp) in [Sym('if'),Sym('lambda'),Sym('quote'),Sym('define')]:
                return form(sexp)
            op = build(car(sexp))
            arg = sexp.cdr.map(build) if sexp.cdr else None#######do sth here#######do sth here
            def get_args(arg,env,cont):
                if nullp(arg):
                    return cont(nil)
                else:
                    return car(arg)(env,lambda v1:get_args(arg.cdr,env,lambda v2:cont(cons(v1,v2))))
            def app(obj,arg,cont):
                if isa(obj,BlkLmd4):
                    raise Exception() 
                    return obj.apply2(arg,cont)
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
print "####part2################"
if 0:
    print eval9(read("""((lambda ()
    (define f (lambda (n s) (if (< n 1) s (f (- n 1) (* n s)))))
    (f 7 1)
    ))""")[0],toplevel.extend())
def peekSexp(code):
    return read(code)
def read1(code):
    return read(code)[0]
class Typ:
    @staticmethod
    def pairp(obj):
        return pairp(obj)
class Scm:
    def __init__(self,toplevel=toplevel):
        self._env = toplevel.extend()
    def sh(self,code):
        return eval9(read(code)[0],self._env)
    def env(self):
        return self._env
    def repl(self):
        while True:
            try:
                print eval(self.sh(raw_input('scm> ')),self._env)
            except Exception as e:
                print e        
    @staticmethod
    def read(sexp):
        return read(code)[0]
    @staticmethod
    def eval(sexp,env):
        return eval9(sexp,env)
    @staticmethod
    def nilEnv(sexp,env):
        return Env()

print eval9(read("""((lambda ()
     (define f (lambda (x) (display "IIIIIIIIIIIIIIIIIIIIIIIIIII") (+ x 1)))
     (display "LLLLLLLLLLLLLLLLLL")
     f
    ))""")[0],toplevel.extend()).apply(cons(1,nil))
print eval(cons(eval9(read("""
((lambda ()
     (define f (lambda () "III"))
     f
))
""")[0],toplevel.extend()),nil),toplevel.extend())
