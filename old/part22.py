#tail-call
from part1 import *
import sys
#sys.setrecursionlimit(100)
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
class PyFun(Prc):
    def __init__(self,func):
        self.func = func
    def __call__(self,*arg):
        return self.func(*arg)
    def apply(self,arg):
        assert pairp(arg) or nullp(arg) ,arg
        #print arg,(arg.toPyList() if arg else [])
        return apply(self.func,(arg.toPyList() if arg else []))
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
            return cons(Sym('quote'),cons(arg,nil))
        return eval9(cons(self,arg and arg.map(quote)),rt)
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
class BlkApp9(BlkLmd9):
    def __init__(self):
        pass
    def __repr__(self):
        return 'LAMBDA '+object.__repr__(self)
    def apply9(self,arg,cont):
        xs = sexpToPyList(arg.cdr)#arg.cdr.cdr.cdr is not None#move to toplevel later
        if len(xs)>1:
            xs = sexpToPyList(arg.cdr)
            arg = cons(arg.car,cons(pyListToSexp(xs[0:-1]+sexpToPyList(xs[-1])),nil))
        if isa(arg.car,BlkLmd9):
            return arg.car.apply9(arg.cdr.car,cont)
        else:
            return cont(arg.car.apply(arg.cdr.car))
##def macroExpend(sexp):
##    pass

##class SymDct(dict):
##    pass SymTbl
def progn(bodys):
    def seq(x,y):
        return lambda env,c:tuk(x,(env,lambda v:y(env,c)))
    def loop(h,t):
        return h if nullp(t) else loop(seq(h,t.car),t.cdr)
    #bodys = sexpbodys.map(build)#build once
    return loop(bodys.car,bodys.cdr)
topmacro = {}
topsform = {}
def dispatch(symtbl,name):
    def _(f):
        symtbl[Sym(name)]=f
    return _
def Ast():
    class ABegin:
        pass
    class ALambda:
        def __init__(self):
            pass
        def dump(self):
            arg = sexp.cdr.car
            bdy = seqs(sexp.cdr.cdr)
            return lambda env,c:tuk(c,(BlkLmd9(arg, bdy ,env),))
    class ADefine:
        pass
    class AValue:
        pass
    class AIdentifier:
        pass
    class AIf:
        def __init__(self,test,then,fail,env):
            self.test,self.then,self.fail = test,then,fail
        def dump(self):
            test,then,fail = self.test.dump(),self.then.dump(),self.fail.dump()
            return lambda env,c:tuk(test,(env,lambda v:then(env,c)if truep(v) else fail(env,c)))
    class AQuote:
        def __init__(self,value):
            self.value = value
        def dump(self):
            value = self.value.dump()
            return lambda env,c:tuk(c,(value,))
topenvrn = Env()
def buildExp10(sexp):
    pass
def buildExp9(sexp):
    def buildSfrom():
        def seqs(sexpbodys):
            def seq(x,y):
                return lambda env,c:tuk(x,(env,lambda v:y(env,c)))
            def loop(h,t):
                if nullp(t):
                    return h
                else:
                    return loop(seq(h,t.car),t.cdr)
            bodys = sexpbodys.map(build)#build once
            return loop(bodys.car,bodys.cdr)
        @dispatch(topsform,'lambda')
        def rLambda(sexp):
            arg = sexp.cdr.car
            #bdy =  progn(sexp.cdr.cdr.map(build))
            bdy = seqs(sexp.cdr.cdr)
            return lambda env,c:tuk(c,(BlkLmd9(arg, bdy ,env),))
            #return lambda env,c:tuk(c,(BlkLmd9(arg, seqs(sexp.cdr.cdr) ,env),))
        @dispatch(topsform,'::if')
        def rIf(sexp):
            #test,then,fail = map(build,sexp.cdr)#build(sexp.cdr.car)
            #test,then,fail = sexp.cdr.map(build)#not use map..rec here,flat it
            test, then, fail = build(sexp.cdr.car), build(sexp.cdr.cdr.car), build(sexp.cdr.cdr.cdr.car)
            #the last one is much faster
            #test = build(sexp.cdr.car)
            #then = build(sexp.cdr.cdr.car)
            #fail = build(sexp.cdr.cdr.cdr.car)
            return lambda env,c:tuk(test,(env,lambda v:then(env,c)if truep(v) else fail(env,c)))
        @dispatch(topsform,'::define')
        def rDefine(sexp):    
            name = sexp.cdr.car
            val = build(sexp.cdr.cdr.car)
            return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))
        @dispatch(topsform,'::begin')#remove from runtime later
        def rBegin(sexp):
            return seqs(sexp.cdr)
        #define-syntax
    ##    elif op==Sym('set!'):
    ##        assert CanUseMset
    ##        name = sexp.cdr.car
    ##        val = build(sexp.cdr.cdr.car)
    ##        return lambda env,c:tuk(val,(env,lambda v:c(env.mset(name,v))))
        @dispatch(topsform,'quote')
        def rQuote(sexp):    
            val = sexp.cdr.car
            return lambda env,c:tuk(c,(val,))
    buildSfrom()
    raw_define = Sym('::define')
    def seqs(sexpbodys):
        def seq(x,y):
            return lambda env,c:tuk(x,(env,lambda v:y(env,c)))
        def loop(h,t):
            if nullp(t):
                return h
            else:
                return loop(seq(h,t.car),t.cdr)
        bodys = sexpbodys.map(build)#build once
        return loop(bodys.car,bodys.cdr)
##    def form(sexp):
##        assert pairp(sexp)
##        op = car(sexp)
##        if op==Sym('::if'):
##            test = build(sexp.cdr.car)
##            then = build(sexp.cdr.cdr.car)
##            fail = build(sexp.cdr.cdr.cdr.car)
##            return lambda env,c:tuk(test,(env,lambda v:then(env,c)if truep(v) else fail(env,c)))
##        elif op==Sym('lambda'):
##            arg = sexp.cdr.car
##            #bodys = sexp.cdr.cdr.map(build)#to one blk
##            #bodyq = lambda env,c:tuk(reduce,(lambda cont,blk:(lambda v:blk(env,cont)),reversed(bodys.toPyList()),c))
##            return lambda env,c:tuk(c,(BlkLmd9(arg, seqs(sexp.cdr.cdr) ,env),))
##        elif op==raw_define:
##            name = sexp.cdr.car
##            val = build(sexp.cdr.cdr.car)
##            return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))
##        elif op==Sym('::begin'):
##            #bodys = sexp.cdr.map(build)
##            return seqs(sexp.cdr)
##            #return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))
##            #return seqs(bodys)
##            #return tukSeqs(bodys)
##            #return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))
##        #define-syntax
##        elif op==Sym('set!'):
##            assert CanUseMset
##            name = sexp.cdr.car
##            val = build(sexp.cdr.cdr.car)
##            return lambda env,c:tuk(val,(env,lambda v:c(env.mset(name,v))))
##        elif op==Sym('quote'):
##            val = sexp.cdr.car
##            return lambda env,c:tuk(c,(val,))
##        raise Exception(sexp)
    def build(sexp):
        if pairp(sexp):
            #if car(sexp) in [Sym('::if'),Sym('lambda'),Sym('quote'),Sym('::begin'),raw_define,Sym('set!')]:
            #    return form(sexp)
            if car(sexp) in topsform:
                return topsform[car(sexp)](sexp)
            if symbolp(car(sexp)) and car(sexp) in topmacro:
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
        elif sexp==Sym('call/cc') or sexp==Sym('call-with-current-continuation'):
            return lambda env,c:tuk(c,(BlkCwcc9(env),))
        elif isa(sexp,Sym):
            return lambda env,c:tuk(c,(env.lookup(sexp),))
        else:
            return lambda env,c:tuk(c,(sexp,))
    return build(sexp)
def eval9(sexp,env):
    #print "eval",sexp
    t=[0]
    def ret(val):
        t[0] = val
        return None,(val,)
    #print "eval9]",buildExp9(sexp)(env,ret)
    tukrun(buildExp9(sexp)(env,ret))
    return t[0]







