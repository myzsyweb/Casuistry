#tail-call
from part1 import *
import sys
sys.setrecursionlimit(5000)
def pyListToSexp(lst):
    return reduce(lambda s,i:cons(i,s),reversed(lst),nil)
def pyListToPair(lst):
    return reduce(lambda s,i:cons(i,s),reversed(lst),nil)
def id(self):
    return self
def broken(x):
    def notImplemented(*a,**b):
        raise NotImplementedError()
    return notImplemented
####class Lambda:
####    def __init__(self,func):
####        self.func=func
####    def __call__(self,*arg,**kw):
####        return self.func(*arg,**kw)
##class IdT:
##    def __repr__(self):
##        return 'Type %s %s'%(self.__class__,tuple.__repr__(self))
class Tuk(tuple):
    def __repr__(self):
        return 'Type %s %s'%(self.__class__,tuple.__repr__(self))
def tuk(cont,arg):
    assert isa(arg,tuple)
    return Tuk((cont,arg))
def cnt(self):
    return self
def runtail(f,x):
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
    return runtail(tuk[0],tuk[1])
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
        rt = self.env.extend(self.arg,arg)#extend here!
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
        pass
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
class Undefined(Err):
    pass
class Env:
    def __init__(self,var=None,bas=None,varnum=0):
        self.bas = bas
        assert var is None
        self.var = var or SymTbl()#only Sym allow
        self.vars=[self.bas]+[None]*varnum
        self.freeze = True if varnum>0 else False
        if self.freeze:
            self.var=None
        self.varsmap=SymTbl()
    def __repr__(self):
        return str((self.var,self.bas))
    def define(self,sym,val):
        assert not self.freeze
        if self.freeze:
            raise Err("It's so cold that I can't understand any new terms.")
        #print "define ",sym
##        if isa(sym,str):
##            sym=Sym(sym)
        #assert sym not in self.var,"I has '%s' already."%sym
        if sym in self.var:# and not CanUseMset:
            raise Err("I has '%s' already."%sym)
        if sym not in self.var:
            self.vars.append(val)
            self.varsmap[sym]=len(self.vars)-1
        else:
            raise None
        self.var[sym] = val;
    def lookup(self,sym):
        assert not self.freeze
        if sym in self.var:
            return self.var[sym]
        elif self.bas is not None:
            return self.bas.lookup(sym)
        else:
            raise Err("I can't understand what '%s' means."%sym)
    def offset(self,sym):
        #assert self.freeze
        if not self.freeze:
            raise Undefined(sym)
        if sym in self.varsmap:
            return [self.varsmap[sym]]
        elif self.bas is not None:
            return [0]+self.bas.offset(sym)
        else:
            raise Undefined(sym)
    def lookupRef(self):
        raise None
    @property
    def varnum(self):
        assert self.freeze
        return len(self.vars)-1
    def freezeIt(self):
        assert not self.freeze
        self.freeze = True
        self.var=self.var
        self.var.__setitem__=None
    def lookupByName(self,sym):
        #assert self.freeze
        if sym in self.var and not self.freeze:
            return self.var[sym]
        if self.bas is not None:
            return self.bas.lookupByName(sym)
        else:
            raise Err("I can't understand what '%s' means."%sym)
    def lookupByOffset(self,offsetChain):
        assert self.freeze
        frame = self
        for i in offsetChain:
            if i==0:
                frame=frame.vars[0]
            else:
                #print i
                return frame.vars[i]
        raise None
    def defineByOffset(self,offsetChain,value):
        assert self.freeze
        assert len(offsetChain)==1
        assert offsetChain[0]>0
        offset = offsetChain[0]
        self.vars[offset]=value    
    def extendByOffset(self,arg=None,val=None,varnum=0):
        env = Env(bas=self,varnum=varnum)
        offset=1
        while pairp(arg):
            env.defineByOffset([offset],car(val))
            arg,val=map(cdr,(arg,val))
            offset+=1
        if not nullp(arg):
            env.defineByOffset([offset],val)
        return env
    def extendDump(self,arg):
        env = Env(bas=self)
        while pairp(arg):
            env.define(car(arg),None)
            arg=arg.cdr
        if not nullp(arg):
            env.define(arg,None)
        return env        
    def extend(self,arg=None,val=None):
        env = Env(bas=self)
        while pairp(arg):
            env.define(car(arg),car(val))
            arg,val=map(cdr,(arg,val))
        if not nullp(arg):
            env.define(arg,val)
        return env
    #give more info here!!!!
def progn(bodys):
    def seq(x,y):
        return lambda env,c:tuk(x,(env,lambda v:y(env,c)))
    def loop(h,t):
        return h if nullp(t) else loop(seq(h,t.car),t.cdr)
    #bodys = sexpbodys.map(build)#build once
    return loop(bodys.car,bodys.cdr)

def dispatch(symtbl,name):
    def _(f):
        symtbl[Sym(name)]=f
    return _

##class AQuote(AstNode):
##    def __init__(self,value):
##        self.value = value
##    def dump(self):
##        value = self.value
##        return lambda env,c:tuk(c,(value,))

def buildExp10(sexp,cenv):
    return build(sexp,cenv)
#def Ast():
class AstNode:#no `build' here must dump before use
    def __init__(self,dumped,cenv):
        #self.cenv=cenv
        self.dumped = dumped
    def dump(self):
        return self.dumped
class ABegin(AstNode):
    def __init__(self,seq,cenv):
        #self.cenv=cenv
        assert isa(seq,Par)
        self.seq = seq
    def dump(self):
        return progn(self.seq.map(lambda x:x.dump()))
##class Lmd(Prc):
##    def __init__(self,lmd,env):
##        self.lmd = lmd
##        self.arg = lmd.cdr.car
##        self.bdy = lmd.cdr.cdr#!!!
##        self.env = env
##    def __repr__(self):
##        return str(self.lmd)
##    def apply(self,arg):
##        #print "body>",self.bdy
##        rt = self.env.extend(self.arg,arg)#entend env here!!!
##        return self.bdy.map(lambda x:eval(x,rt)).toPyList()[-1]
##        #fold-left
##        #return eval(self.bdy,self.env.extend(self.arg,arg))  
class AApply(AstNode):
    def __init__(self,proc,arg,cenv):
        #self.cenv=cenv
        assert isa(proc,AstNode)
        assert isa(arg,Par) or arg is None
        self.proc,self.arg = proc,arg
    def dump(self):
        def apply_args(arg,env,cont):
            return cont(nil) if nullp(arg) else car(arg)(env,lambda v1:apply_args(arg.cdr,env,lambda v2:cont(cons(v1,v2))))
        def app(obj,arg,cont):
            return obj.apply9(arg,cont) if isa(obj,BlkLmd9) else cont(obj.apply(arg))
        op = self.proc.dump()
        arg = self.arg.map(lambda x:x.dump()) if self.arg else None
        return lambda env,c:tuk(op,(env,lambda v1:apply_args(arg,env,lambda v2:app(v1,v2,c))))     
class AIf(AstNode):
    def __init__(self,test,then,fail,cenv):
        #self.cenv=cenv
        assert isa(test,AstNode)
        assert isa(then,AstNode)
        assert isa(fail,AstNode)
        self.test,self.then,self.fail = test,then,fail
    def dump(self):
        test,then,fail = self.test.dump(),self.then.dump(),self.fail.dump()
        return lambda env,c:tuk(test,(env,lambda v:then(env,c) if truep(v) else fail(env,c)))
class AValue(AstNode):
    def __init__(self,value,cenv):
        #self.cenv=cenv
        self.value = value
    def dump(self):
        value = self.value
        return lambda env,c:tuk(c,(value,))
    #####feature_local#####
feature_local=0
class PrcLocalLmd(Prc):
    def __init__(self,arg,blk,env,varnum):
        self.arg = arg
        self.bdy = blk#getStmt()
        self.env = env
        #assert env.freeze
        self.varnum=varnum
    def __repr__(self):
        return 'LAMBDA '+object.__repr__(self)
    def __call__(self,*arg):
        print ">>>",pyListToSexp(arg)
        return self.apply(pyListToSexp(arg))
    @broken
    def apply(self,arg):
        rt = self.env.extendByOffset(self.arg,arg,self.varnum)#extend here!
        assert rt.freeze
        def quote(arg):
            return cons(Sym('quote'),cons(arg,nil))
        return eval9(cons(self,arg and arg.map(quote)),rt)
    def apply9(self,arg,cont):
        #rt = self.env.extend(self.arg,arg)#extend here!
        rt = self.env.extendByOffset(self.arg,arg,self.varnum)#extend here!
        assert rt.freeze
        #print "????",self.bdy(rt,cont)
        return self.bdy(rt,cont)
class ALambda(AstNode):
    def __init__(self,arg,bdy,cenv):
        self.cenv=cenv#here
        assert isa(arg,Par) or isa(arg,Sym) or arg is None
        assert isa(bdy,Par)
        self.arg,self.bdy=arg,bdy
    def dump(self):
        arg = self.arg
        #bdy = progn(self.bdy.map(lambda x:x.dump()))
        rtcenv = self.cenv.extendDump(self.arg)#new r
        buildbody = self.bdy.map(lambda x:build(x,rtcenv))
        #bdy = progn(self.bdy.map(lambda x:build(x,rtcenv).dump()))#build here
        rtcenv.freezeIt()#important for speeed
        #rtcenv.define(Sym('a'),1) fail here
        bdy = progn(buildbody.map(lambda x:x.dump()))
        #print rtcenv.varnum
        #PrcLocalLmd
        #varnum = self.cenv.varnum
        varnum = rtcenv.varnum
        if feature_local:
            return lambda env,c:tuk(c,(PrcLocalLmd(arg, bdy ,env,varnum),))
        return lambda env,c:tuk(c,(BlkLmd9(arg, bdy ,env),))
        #return lambda env,c:tuk(c,(PrcLocalLmd(arg, bdy ,env,varnum),))
class ADefine(AstNode):
    def __init__(self,name,val,cenv):
        self.cenv=cenv
        assert isa(name,Sym)
        assert isa(val,AstNode)
        self.name,self.val=name,val
    def dump(self):
        name,val = self.name,self.val.dump()
        if self.cenv.freeze and feature_local:
            offset = self.cenv.offset(name)#must find one
            return lambda env,c:tuk(val,(env,lambda v:c(env.defineByOffset(name,v))))
        return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))
        #self.cenv.define(name,None)#define here!
        #print "define>",name
        #return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))
class AIdentifier(AstNode):
    def __init__(self,name,cenv):
        self.cenv=cenv
        self.name = name
    def dump(self):
        name = self.name
        if self.cenv.freeze and feature_local:
            try:
                offset = self.cenv.offset(name)
                return lambda env,c:tuk(c,(env.lookupByOffset(offset),))
            except Undefined as e:
                return lambda env,c:tuk(c,(env.lookupByName(name),))
        
        #tryoffset
        #print "dump>var>",self.cenv.lookup(name)
        #return lambda env,c:tuk(c,(env.lookupByOffset(env.offset(name)),))
        return lambda env,c:tuk(c,(env.lookup(name),))
##class ALocalLambda(AstNode):
##    def __init__(self,arg,bdy,cenv):
##        self.cenv=cenv#here
##        assert isa(arg,Par) or isa(arg,Sym) or arg is None
##        assert isa(bdy,Par)
##        self.arg,self.bdy=arg,bdy
##    def dump(self):
##        arg = self.arg
##        #bdy = progn(self.bdy.map(lambda x:x.dump()))
##        rtcenv = self.cenv.extendDump(self.arg)#new r
##        #print "newruntime "*5
##        buildbody = self.bdy.map(lambda x:build(x,rtcenv))
##        #bdy = progn(self.bdy.map(lambda x:build(x,rtcenv).dump()))#build here
##        rtcenv.freezeIt()#importtant for speeed
##        #rtcenv.define(Sym('a'),1) fail here
##        bdy = progn(buildbody.map(lambda x:x.dump()))
##        #print rtcenv.varnum
##        #PrcLocalLmd
##        varnum = self.cenv.varnum
##        return lambda env,c:tuk(c,(BlkLmd9(arg, bdy ,env),))
##        return lambda env,c:tuk(c,(PrcLocalLmd(arg, bdy ,env,varnum),))
##@broken
##class ALocalSetter(AstNode):#ALocalDefine
##    def __init__(self,name,cenv):
##        self.cenv=cenv
##        self.name = name
##    def dump(self):
##        name = self.name
##        try:
##            offset = self.cenv.offset(name)
##            return lambda env,c:tuk(c,(env.lookupByOffset(offset),))
##        except Undefined as e:
##            return lambda env,c:tuk(c,(env.lookup(name),))
##        #print "dump>var>",self.cenv.lookup(name)
##        #return lambda env,c:tuk(c,(env.lookupByOffset(offset),))
##        return lambda env,c:tuk(c,(env.lookupByOffset(env.offset(name)),))
##@broken    
##class ALocalDefine(AstNode):
##    def __init__(self,name,val,cenv):
##        self.cenv=cenv
##        assert isa(name,Sym)
##        assert isa(val,AstNode)
##        self.name,self.val=name,val
##    def dump(self):
##        name,val = self.name,self.val.dump()
##        offset=self.cenv.offset(name)
##        return lambda env,c:tuk(val,(env,lambda v:c(env.defineByOffset(env.offset(name),v))))
##        return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))   
##@broken    
##class ALocalIdentifier(AstNode):
##    def __init__(self,name,cenv):
##        self.cenv=cenv
##        self.name = name
##    def dump(self):
##        name = self.name
##        try:
##            offset = self.cenv.offset(name)
##            return lambda env,c:tuk(c,(env.lookupByOffset(offset),))
##        except Undefined as e:
##            return lambda env,c:tuk(c,(env.lookup(name),))
@broken
class ALocalRef(AstNode):#LValue/RValue
    def __init__(self,name,cenv):
        self.cenv=cenv
        self.name = name
    def dump(self):
        name = self.name
        #offset = self.offset
        #print "dump>var>",self.cenv.lookup(name)
        #return lambda env,c:tuk(c,(env.lookupByOffset(offset),))
        return lambda env,c:tuk(c,(env.lookupByOffset(env.offset(name)),))

topsform = {}
def buildSfrom():
##        @dispatch(topsform,'lambda')
##        def rLambda(sexp,cenv):
##            #return ALambda(sexp.cdr.car,sexp.cdr.cdr,cenv=cenv)
##            return ALambda(sexp.cdr.car,sexp.cdr.cdr.map(build),cenv=cenv)#use abegin later?
    @dispatch(topsform,'::if')
    def rIf(sexp,cenv):
        return AIf(build(sexp.cdr.car,cenv), build(sexp.cdr.cdr.car,cenv), build(sexp.cdr.cdr.cdr.car,cenv),cenv=cenv)
    @dispatch(topsform,'::define')
    def rDefine(sexp,cenv):
        raise None
        return ADefine(sexp.cdr.car,build(sexp.cdr.cdr.car),cenv=cenv)
    @dispatch(topsform,'::begin')#remove later!
    def rBegin(sexp,cenv):
        return ABegin(sexp.cdr.map(lambda x:build(x,cenv)),cenv=cenv)
    @dispatch(topsform,'quote')
    def rQuote(sexp,cenv):
        return AValue(sexp.cdr.car,cenv=cenv)
buildSfrom()
def build(sexp,cenv):
    if pairp(sexp):
        #print "@%s@"%car(sexp) ,
        if car(sexp) is Sym('::define'):
            #raise None
            cenv.define(sexp.cdr.car,None)
            #print "define>",sexp.cdr.car
            #print "#"*255
            return ADefine(sexp.cdr.car,build(sexp.cdr.cdr.car,cenv),cenv=cenv)
        if car(sexp) is Sym('lambda'):
            #newcenv=cenv.extendDump(sexp.cdr.car)
            return ALambda(sexp.cdr.car,sexp.cdr.cdr,cenv=cenv)#move build to dump
            #return ALambda(sexp.cdr.car,sexp.cdr.cdr.map(lambda x:build(x,newcenv)),cenv=cenv)#move buiid to dump
        if car(sexp) in topsform:
            return topsform[car(sexp)](sexp,cenv)
        if symbolp(car(sexp)) and car(sexp) in topmacro:
            return topmacro[car(sexp)](sexp)
            return AstNode(topmacro[car(sexp)](sexp),cenv=cenv)
        return AApply(build(car(sexp),cenv),sexp.cdr.map(lambda x:build(x,cenv)) if sexp.cdr else None,cenv=cenv)
    elif sexp is Sym('call/cc') or sexp is Sym('call-with-current-continuation'):
        return AstNode(lambda env,c:tuk(c,(BlkCwcc9(env),)),cenv=cenv)
    elif isa(sexp,Sym):
        local = 0
        if local:
            return ALocalIdentifier(sexp,cenv)
####            print "lookup ",sexp
##        try:
##            pass
##            offset = cenv.offset(sexp)
##            #return ALocalIdentifier(offset,cenv)
##            #print offset,
##        except Undefined as e:
##            pass
##            #print e
        return AIdentifier(sexp,cenv=cenv)
    else:
        return AValue(sexp,cenv=cenv)
#return build(sexp,cenv)
#===============================================================================================#
topmacro = {}
#topsform = {}
topenvrn = Env()
if 0:
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
def eval9(sexp,env=Env()):
    #print "eval",sexp
    t=[0]
    def ret(val):
        t[0] = val
        return None,(val,)
    #print "eval9]",buildExp9(sexp)(env,ret)
    #tukrun(buildExp9(sexp)(env,ret))
    tukrun(buildExp10(sexp,cenv=Env()).dump()(env,ret))
    return t[0]

print eval9(read('1')[0])
print eval9(read('(::define a 1)')[0])
print buildExp10(read('(::define a 1)')[0],Env())




