from T import *
import T
import sys
sys.setrecursionlimit(600)
def pyListToSexp(lst):
    return Par.fromIter(lst)
    #return reduce(lambda s,i:cons(i,s),reversed(lst),nil)
##def pyListToPair(lst):
##    return reduce(lambda s,i:cons(i,s),reversed(lst),nil)
def id(self):
    return self
def broken(x):
    def notImplemented(*a,**b):
        raise NotImplementedError()
    return notImplemented
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
        f, x = f(*x)
    return x
def tukrun(tuk):
    assert isa(tuk,Tuk)
    return runtail(tuk[0],tuk[1])
class BlkLmd9(Prc):
    def __init__(self,arg,blk,env):
        self.arg = arg
        self.bdy = blk#getStmt()
        self.env = env
    def __repr__(self):
        return 'LAMBDA '+object.__repr__(self)
    def __call__(self,*arg):
        #print ">>>",pyListToSexp(arg)
        return self.apply(pyListToSexp(arg))
    def apply(self,arg):#call apply9 then
        rt = self.env.extend(self.arg,arg)
        def quote(arg):
            return cons(Sym('quote'),cons(arg,nil))
        return eval9(cons(self,arg and arg.map(quote)),rt)
    #@broken
    def apply9(self,arg,cont):
        #raise None
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
    def __repr__(self):
        return "LAMBDA 'call/cc'"
    def apply(self,arg):
        BlkLmd9.apply(self,arg)
        raise Exception()
    def apply9(self,arg,cont):
        if not isa(arg.car,BlkLmd9):
            raise Err()
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
class Undefined(Err):#remove later
    pass
from collections import OrderedDict
class Globe:
    pass
class Frame:#list
    def __init__(self,glob=None,upvars=tuple(),varnum=0):
        self.glob = glob
        self.vars=[True]+[None]*varnum
        self.upvars=upvars
    @property
    def freeze(self):
        return True
    def lookupGlob(self,sym):
        assert isa(sym,Sym)
        return self.glob.lookup(sym)
    def lookupLocal(self,offset):
        assert isa(offset,int)
        return self.vars[offset]
    def lookupUplocal(self,offset):
        assert isa(offset,int)
        return self.upvars[offset]
    def defineLocal(self,offset,value):
        assert self.vars[offset] is None
        self.vars[offset]=value
    def extendFrame(self,arg=None,val=None,varnum=0,upvars=tuple()):
        frame = Frame(glob=self.glob,varnum=varnum,upvars=upvars)
        offset=1
        while pairp(arg):
            frame.defineLocal(offset,car(val))
            arg,val=map(cdr,(arg,val))
            offset+=1
        if not nullp(arg):
            frame.defineLocal(offset,val)
        return frame
class Env:#split methods to small piece functions
    def __init__(self,var=None,bas=None,varnum=None):
        self.bas = bas
        assert var is None
        self.vars=[self.bas]+[None]*(varnum if varnum is not None else 0)
        self._freeze = True if varnum is not None else False
        self.freeze = self._freeze
        if self.freeze:
            self.var = None#remove later
            self.varsmap = None
        else:
            self.var = var or SymTbl()#only Sym allow,remove later
            self.varsmap=SymTbl()
        if feature_local2:
            self.uplocal=OrderedDict()
            self.uplocals=[]#use self.vars[0] later and let self.bas to my father
    def __repr__(self):
        return str((self.var,self.bas))
    def define(self,sym,val):
        assert not self.freeze
        if sym in self.var:
            raise Err("I has '%s' already."%sym)
        else:
            self.vars.append(val)
            self.varsmap[sym]=len(self.vars)-1
            self.var[sym] = val
    def lookup(self,sym):
        if self.freeze:
            offset = self.offset(sym)
            if offset is None:
                return self.lookupByName(sym)
            else:
                return self.lookupByOffset(offset)
        else:
            if sym in self.var:
                return self.var[sym]
            elif self.bas is not None:
                return self.bas.lookup(sym)
        raise Err("I can't understand what '%s' means."%sym)
    def offset(self,sym):
        if not self.freeze:
            return None
        if self.varsmap is None:#bug!
            return None
        #assert self.varsmap is not None,sym
        if sym in self.varsmap:
            return [self.varsmap[sym]]
        elif self.bas is not None:
            offset=self.bas.offset(sym)
            if offset is None:
                if feature_local2:
                    self.uplocal[sym]=None
                return None
            return [0]+offset
        else:
            return None
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
        assert self.freeze
        if self.bas is not None:
            return self.bas.lookup(sym)
        else:
            raise Err("I can't understand what '%s' means."%sym)
    def lookupByOffset(self,offsetChain):
        assert self.freeze
        frame = self
        for i in offsetChain:
            if i==0:
                frame=frame.vars[0]
            else:
                return frame.vars[i]
        raise None
    def defineByOffset(self,offsetChain,value):
        assert self.freeze
        assert len(offsetChain)==1
        assert offsetChain[0]>0
        offset = offsetChain[0]
        self.vars[offset]=value    
    def extendByOffset(self,arg=None,val=None,varnum=None):
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
    def lookupLocal(self,place):
        return self.vars[place]
    def lookupUplocal(self,place):
        return self.uplocals[place]
    def lookupOffsetLocal(self,sym):
        try:
            if sym in self.varmaps:
                return self.varmaps[sym]
        except AttributeError:
            print "d"
##        try:
##            if sym in self.uplocal:
##                return (0,self.uplocal[sym])
##        except AttributeError:
##            print "d"
        if sym in self.bas.uplocal:
            return (0,self.uplocal[sym])
        assert None
        #self.varmaps
        #self.uplocal
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

def buildExp10(sexp,cenv):
    return build(sexp,cenv)
#def Ast():
class AstNode:#no `build' here must dump before use
    def __init__(self,dumped,cenv):
        #self.cenv=cenv
        self.dumped = dumped
    def dump(self):
        return self.dumped
class ABegin(AstNode):#lat lambda use it
    def __init__(self,seq,cenv):
        #self.cenv=cenv
        assert isa(seq,Par)
        self.seq = seq
    def dump(self):
        return progn(self.seq.map(lambda x:x.dump()))  
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
#####==================================feature_local===================================#####
#feature_local=1#must be 1
feature_local2=0
####======================FLAG=======#####
class PrcLocalLmd(Prc,BlkLmd9):
    def __init__(self,arg,blk,env,varnum,upvars=tuple()):
        self.arg = arg
        self.bdy = blk#getStmt()
        self.env = env
        #assert env.freeze
        self.varnum=varnum
        self.upvars=upvars
        if feature_local2:
            self.localnum=varnum
            self.uplocalnum=0
    def __repr__(self):
        return 'LAMBDA '+object.__repr__(self) 
    def __call__(self,*arg):
        print ">>>",pyListToSexp(arg)
        return self.apply(pyListToSexp(arg))
    def apply(self,arg):
        if feature_local2:
            rt = self.env.extendFrame(self.arg,arg,upvars=self.upvars,varnum=self.varnum)       
        else:
            rt = self.env.extendByOffset(self.arg,arg,self.varnum)#extend here!
        assert rt.freeze
        def quote(arg):
            return cons(Sym('quote'),cons(arg,nil))
        return eval9(cons(self,arg and arg.map(quote)),rt)#use apply_arg later
    def apply9(self,arg,cont):
        if feature_local2:
            rrt = self.env.extendFrame(self.arg,arg,upvars=self.upvars,varnum=self.varnum)
            assert rrt.freeze
            return self.bdy(rrt,cont)
        rt = self.env.extendByOffset(self.arg,arg,self.varnum)#extend here!
        assert rt.freeze
        return self.bdy(rt,cont)
class ALambda(AstNode):
    def __init__(self,arg,bdy,cenv):
        self.cenv=cenv#here
        assert isa(arg,Par) or isa(arg,Sym) or arg is None
        assert isa(bdy,Par)
        self.arg,self.bdy=arg,bdy          
    def dump(self):
        arg = self.arg
        rtcenv = self.cenv.extendDump(self.arg)#new r
        buildbody = self.bdy.map(lambda x:build(x,rtcenv))#build here
        rtcenv.freezeIt() #for speeed
        bdy = progn(buildbody.map(lambda x:x.dump()))#dump here
        varnum = rtcenv.varnum#some runtime info
        if feature_local2:
            upvarsmap=[cenv.uplocal.keys().index(i) for i in rtcenv.uplocal.keys()]
            def tukLambda(env,c):
                #not work right yet
                upvars=[env.lookupUplocal(i) for i in upvarsmap]
                return tuk(c,(PrcLocalLmd(arg, bdy ,env,varnum,upvars),))
            return tukLambda
        return lambda env,c:tuk(c,(PrcLocalLmd(arg, bdy ,env,varnum),))#use env to find local
class AIdentifier(AstNode):
    def __init__(self,name,cenv):
        self.cenv=cenv
        self.name = name
    def dump(self):
        name = self.name
        if self.cenv.freeze:
            offset = self.cenv.offset(name)#if being my local or my parent's local
            if offset is None:
                return lambda env,c:tuk(c,(env.lookupByName(name),))#is glob
            if feature_local2:
                if offset[0]==0:
                    place=self.cenv.uplocal.keys().index(name)
                    return lambda env,c:tuk(c,(env.lookupUplocal(place),))
                else:
                    place = offset[0]
                    return lambda env,c:tuk(c,(env.lookupLocal(place),))

            return lambda env,c:tuk(c,(env.lookupByOffset(offset),))
        else:#if glob is found use AValue here
            return lambda env,c:tuk(c,(env.lookup(name),))#bug here!
        assert None
class ADefine(AstNode):
    def __init__(self,name,val,cenv):
        self.cenv=cenv
        assert isa(name,Sym)
        assert isa(val,AstNode)
        cenv.define(name,None)#move here
        self.name,self.val=name,val
    def dump(self):
        name,val = self.name,self.val.dump()
        if self.cenv.freeze:
            offset = self.cenv.offset(name)#must find one
            return lambda env,c:tuk(val,(env,lambda v:c(env.defineByOffset(offset,v))))
        else:
            return lambda env,c:tuk(val,(env,lambda v:c(env.define(name,v))))
topsform = {}
def buildSfrom():
##        @dispatch(topsform,'lambda')#use abegin later?
    @dispatch(topsform,'::if')
    def rIf(sexp,cenv):
        return AIf(build(sexp.cdr.car,cenv), build(sexp.cdr.cdr.car,cenv), build(sexp.cdr.cdr.cdr.car,cenv),cenv=cenv)
    @dispatch(topsform,'::begin')#remove later!
    def rBegin(sexp,cenv):
        return ABegin(sexp.cdr.map(lambda x:build(x,cenv)),cenv=cenv)
    @dispatch(topsform,'quote')
    def rQuote(sexp,cenv):
        return AValue(sexp.cdr.car,cenv=cenv)
buildSfrom()
def build(sexp,cenv,macro=None):
    if pairp(sexp):
        if car(sexp) is Sym('::define'):
            #cenv.define(sexp.cdr.car,None)#move to node
            return ADefine(sexp.cdr.car,build(sexp.cdr.cdr.car,cenv),cenv=cenv)
        elif car(sexp) is Sym('lambda'):
            #newcenv=cenv.extendDump(sexp.cdr.car)
            return ALambda(sexp.cdr.car,sexp.cdr.cdr,cenv=cenv)#move build to dump
            #return ALambda(sexp.cdr.car,sexp.cdr.cdr.map(lambda x:build(x,newcenv)),cenv=cenv)
        elif macro is None and car(sexp) is Sym('defmacro') or  car(sexp) is Sym('defmarco'):#misspell
            defmacro(sexp)
            return AValue(None,cenv=cenv)
            return AValue(defmacro(sexp),cenv=cenv)
        elif car(sexp) in topsform:
            return topsform[car(sexp)](sexp,cenv)
        elif symbolp(car(sexp)) and car(sexp) in topmacro:
            return topmacro[car(sexp)](sexp,cenv)
            #return AstNode(topmacro[car(sexp)](sexp),cenv=cenv)
        else:
            return AApply(build(car(sexp),cenv),sexp.cdr.map(lambda x:build(x,cenv)) if sexp.cdr else None,cenv=cenv)
    elif sexp is Sym('call/cc') or sexp is Sym('call-with-current-continuation'):
        return AstNode(lambda env,c:tuk(c,(BlkCwcc9(env),)),cenv=cenv)
    elif isa(sexp,Sym):
        return AIdentifier(sexp,cenv=cenv)
    else:
        return AValue(sexp,cenv=cenv)
#return build(sexp,cenv)
#===============================================================================================#
topmacro = {}
def defmacro(sexp):#not use outside,due to scope
    assert sexp.car==Sym('defmarco') or sexp.car==Sym('defmacro')#shoud defmacro
    name,marco_rule = sexp.cdr.car,cons(Sym('lambda'),sexp.cdr.cdr)
    def expend(sexp,cenv):
        #return buildExp10(Scm.eval(marco_rule,topenvrn).apply(sexp.cdr),cenv)
        trans = Scm.eval(marco_rule,topenvrn)#late here
        expended_code = trans.apply(sexp.cdr)
        return buildExp10(expended_code,cenv)
    topmacro[name] = expend
#topsform = {}
topenvrn = Env()
def eval9(sexp,env=Env()):
    return tukrun(buildExp10(sexp,cenv=Env()).dump()(env,lambda x:(None,x)))
class Scm:
    def __init__(self,toplevel=None):
        toplevel=toplevel if toplevel else topenvrn
        self._env = toplevel.extend()
    def sh(self,code):
        return eval9(peekSexp("(::begin %s)"%code)[0],self._env)
    @staticmethod    
    def load(filename,env):
        with open(filename) as f:
            return Scm.eval(Scm.read("(::begin %s)"%f.read()),env)#?
    @staticmethod 
    def fastLoad(self):
        pass
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
        return peekSexp(sexp)[0]
    @staticmethod
    def eval(sexp,env):
        return eval9(sexp,env)
    @staticmethod
    def nilEnv(sexp,env):
        return Env()

def block(f):
    return f()

##    def loadMacro(filename):#move to eval but limit
##        with open(filename) as f:
##            code = f.read()
##            start = 0
##            while 1:
##                t,end = peekSexp(code,start)
##                if end==-1:
##                    break
##                defmacro(code[start:end])
##                start = end 
##    loadMacro("initsyx.scm")

eval9(peekSexp('1')[0])
eval9(peekSexp('(::define a 1)')[0])
buildExp10(peekSexp('(::define a 1)')[0],Env())
defmacro(T.peekSexp("""(defmarco begin lst (cons '::begin lst))""")[0])
@block
def initMacro():
    Scm.load("initsyx.scm",topenvrn)
    Scm.load("quasiquote.scm",topenvrn)
    Scm.load("do.scm",topenvrn)
    Scm.load("initsyn2.scm",topenvrn)

###################################################################
topenvrn.define(Sym("apply"),BlkApp9())##
#define("apply",BlkApp9())
import P
P.makePrim(lambda k,v:topenvrn.define(k,v),topenvrn,Scm)
