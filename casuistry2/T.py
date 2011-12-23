#!python27
##############info#######################
"""
@author ee.zsy
@date Nov.25,2011
@date Nov.27,2011
"""
##############todo#######################
#principle
#write test code first!
#keep simple,flat
#perfer to use class but not too many method
#one piece code do one thing,independent
#not do anything not necessary
#api can change/export later,let it work first
#just add sth. in some place with new name or new case
#impl the most simple case,then dispatch
#not follow the principle

#list
#apply
#string
#calc 24
#tail-rec
#call/cc
#export api
#__all__=[]
#public = lambda func:__all__.append(func.__name__)
##def isa(obj,typ):
##    return isinstance(obj,typ)
isa=isinstance
#######################lex#########################
#|(?P<cmt>;[^\n\r]*[\n\t])
#|(?P<int>[-+]?\d+)
#|(?P<fix>[-+]?\d+(/\d+)?)
#|(?P<flo>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)
import re
pattern = r'''
 (?P<lpr>\()
|(?P<rpr>\))
|(?P<qte>\')
|(?P<qqt>`)
|(?P<uqs>,@)
|(?P<uqt>,)
|(?P<blt>\#[tT])
|(?P<blf>\#[fF])
|(?P<chr>\#\\.[^ \)\t\n\r]*)
|(?P<shr>\#)
|(?P<num>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)
|(?P<str>\"(\\.|[^"])*\")
|(?P<wht>([ \t\n\r]+)|(;.*?[\n\r]))
|(?P<sym>[^ ;\)\(\t\n\r]+)
'''
token = re.compile(pattern,re.S|re.X)
def peekToken(text,start=0):
    regex = token.match(text,start)
    if regex:
        tag = [(k,v) for k,v in regex.groupdict().items() if v]
        return tag[0],regex.end()
    return None,None
##peekToken(code)
def printTokens(code):
    tmp = code
    nxt = 0
    while nxt is not None:
        tag,nxt = peekToken(tmp,nxt)
        print tag
#tokenTest(code)
#########################type####################
class Err(Exception):
    pass
def check(true,err):
    if not true:
        raise err
    return True
class Obj:
    pass
nil = None
CanUseMset = True and False and False
##TypePairImpl = tuple
##if CanUseMset:
##    TypePairImpl = list
def cons(car,cdr):
    return Par.cons(car,cdr)
def car(pair):
    #assert is(pair,Par)
    #return pair[0]
    return pair.car
def cdr(pair):
    #check()
    #return pair[1]
##    if not pairp(pair):
##        raise Err()
    return pair.cdr
def mset_car(pair,val):
    assert CanUseMset
    pair.car=val
def mSetCar(pair,val):
    assert CanUseMset
    pair.car=val
def mset_cdr(pair,val):
    assert CanUseMset
    pair.cdr=val
def mSetCar(pair,val):
    assert CanUseMset
    pair.cdr=val
def nullp(obj):
    return obj is None
def pairp(pair):
    return isa(pair,Par)
def sexpToPyList(pair):
    return pair.toPyList()if pair else []
##    pyList = []
##    while not nullp(pair):
##        pyList.append(car(pair))
##        pair = cdr(pair)
##    return pyList
def pairToPyList(pair):
    return pair.toPyList()if pair else []
##    pyList = []
##    while not nullp(pair):
##        pyList.append(car(pair))
##        pair = cdr(pair)
##    return pyList
    #must no rec here!
def listp(lst):
    if nullp(lst):
        return True
    elif pairp(lst) and nullp(lst.cdr):
        return True
    elif pairp(lst.cdr):
        return listp(cdr(lst))
    return False
##class T:
##    @staticmethod
##    def map():
##        pass
##    pass
class Chr(str):#not use it,do as python do
    def toPyInt(self):
        return ord(self)
    def toPyStr(self):
        return self
def charp(ch):
    return isa(ch,str) and len(ch)==1#use int later to support unicode
from collections import Iterable
class Par(Iterable):#(TypePairImpl):
    def __init__(self,pair):
        self._val = pair
    @property
    def car(self):
        return self._val[0]
    @property
    def cdr(self):
        return self._val[1]
    @staticmethod
    def cons(car,cdr):
        return Par((car,cdr))
##    @car.setter
##    def car(self,val):
##        assert CanUseMset
##        self._val[0]=val
##    @cdr.setter
##    def cdr(self,val):
##        assert CanUseMset
##        self._val[1]=val
    def __repr__(self):
        return "(%s . %s)"%(self.car,self.cdr)
    def map(self,pred):
        return Par.cons(pred(self.car),self.cdr.map(pred) if self.cdr else None)
    def toPyList(self):
        #return list(self)
        #assert listp(self)
        pair,pyList = self,[]
        while pair:
            pyList.append(pair.car)
            pair = pair.cdr
        return pyList
    def __eq__(self,obj):
        return isa(obj,Par) and self._val==obj._val
    @staticmethod
    def fromIter(lst):
        return reduce(lambda s,i:Par.cons(i,s),reversed(lst),nil)
    def __iter__(self):
        def iter(self):
            while pairp(self):
                yield self.car
                self = self.cdr
            assert nullp(self)
        return iter(self)
from weakref import WeakValueDictionary
class Sym(object):#(str):
    c = {}#WeakValueDictionary()
    def __new__(cls,sym):
        assert isa(sym,str)
        sym = sym.upper()
        inst = cls.c.get(sym,None)
        if inst is None:
            inst = object.__new__(cls)
            cls.c[sym] = inst
        return inst
    def __str__(self):
        return [k for k,v in Sym.c.items() if v is self][0]
    def __repr__(self):
        return str(self)
def symbolp(sym):
    return isa(sym,Sym)
class Str(str):
    pass
def stringp(obj):
    return isa(obj,str) and not isa(obj,Sym)
from fractions import Fraction
from numbers import Number
def numberp(x):
    return isa(x,Number)
class Num(Fraction):
    def __repr__(self):
        return str(self)
##class NumInt(Fraction):#int/long
##    pass
class NumFix(Fraction):#int/long
    pass
class NumFlo(float):
    pass
class NumCpx(complex):
    pass
class Vec(list):
    pass
def vectorp(vec):
    return isa(vec,list) or isa(vec,tuple) or isa(vec,Vec)
class Tbl(dict):#table
    pass
class Ref:#too slow
    def __init__(self):
        self.undefined=True
    def get(self):
        if self.undefined:
            raise Err('Undefined')
        return self._val
    def set(self,val):
        self.undefined=False
        self._val=val
        return self
    @property
    def defined(self):
        return not self.undefined
    def type(self):
        return type(self)
class Bol:
    pass
def truep(bol):
    return bol is not False
def booleanp(bol):
    return bol is True or bol is False
class SymTbl(dict):
    def __setitem__(self,key, val):
        assert isa(key,Sym)
        return dict.__setitem__(self,key,val)
##if 0:
##    #EnvReflection
##    class Env:
##        def __init__(self,var=None,bas=None):
##            self.bas = bas
##            self.var = var or SymTbl()#only Sym allow
##            self.vars=[None]
##        def __repr__(self):
##            return str((self.var,self.bas))
##        def define(self,sym,val):
##            #print "define ",sym
##    ##        if isa(sym,str):
##    ##            sym=Sym(sym)
##            #assert sym not in self.var,"I has '%s' already."%sym
##            if sym in self.var:# and not CanUseMset:
##                raise Err("I has '%s' already."%sym)
##            if sym not in self.var:
##                self.vars.append(val)
##            self.var[sym] = val;
##        def lookup(self,sym):
##            if sym in self.var:
##                return self.var[sym]
##            elif self.bas is not None:
##                return self.bas.lookup(sym)
##            else:
##                raise Err("I can't understand what '%s' means."%sym)
##        def offset(self,sym):
##            return 0
##        def extend(self,arg=None,val=None):
##            #print "extend>",arg,val
##            # "extend>",arg,val.car if val else None
##            #var = {}
##            env = Env(bas=self)
##            while pairp(arg):
##                #var[car(arg)]=car(val)
##                env.define(car(arg),car(val))
##                arg,val=map(cdr,(arg,val))
##            if not nullp(arg):
##                #var[arg]=val
##                env.define(arg,val)
##            #print "extend>",var
##            return env
##            #return Env(var,self)
##        #give more info here!!!!
##    ##    def mset(self,sym,val):
##    ##        if not CanUseMset:
##    ##            raise Err("set!")
##    ##        print "set %s to %s"%(val,sym)
##    ##        self.var[sym] = val
class Prc:
    def __init__(self,pred=None):
        self.pred = pred
    def apply(self,arg):
        assert pairp(arg) or nullp(arg)
        if self.pred:
            return self.pred(arg)
        else:
            raise NotImplementedError()
def procedurep(obj):
    return isa(obj,Prc)
class Reader:
    pass
class SyxErr(Exception):
    pass
class Eof:
    pass
def peekSexp(text,start=0):
    def sexp(s,pos):
        #print s[pos:]
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
            return Str(tag[1][1:-1].replace(r'\"','"')),end
        elif tag[0]=='qte':
            exp,end = sexp(s,end)
            if end==-1:
                return "syx err",-1
            return Par((Sym("quote"),Par.cons(exp,None))),end
        elif tag[0]in ('qqt','uqt','uqs'):
            sym={'qqt':'quasiquote','uqt':'unquote','uqs':'unquote-splicing'}
            exp,end = sexp(s,end)
            if end==-1:
                return "syx err",-1
            return Par((Sym(sym[tag[0]]),Par.cons(exp,None))),end
        elif tag[0]=='lpr':
            exp,end = srst(s,end)
            if end==-1:
                return "syx err",-1
            return (exp),end
        elif tag[0]=='shr':
            exp,end = sshr(s,end)
            if end==-1:
                return "syx err",-1
            return exp,end
        elif tag[0]=='blt':
            return True,end
        elif tag[0]=='blf':
            return False,end
        elif tag[0]=='chr':
            if len(tag[1])==3:
                return Chr(tag[1][2]),end
            elif tag[1].lower()==r'#\space':
                return Chr(' '),end
            elif tag[1].lower()==r'#\newline':
                return Chr('\n'),end
            raise SyxErr("not a char")
        raise SyxErr(tag,end,s[pos:end])
    def srst(s,pos):
        tag,end = peekToken(s,pos)
        if not tag:
            return "$",-1
        if tag[0]=='wht':
            return srst(s,end)
        elif tag[0]=='rpr':
            return nil,end
        elif tag==('sym','.'):
            return sdot(s,end)
        else:
            exp,end = sexp(s,pos)
            if end==-1:
                return "syx err",-1
            exp2,end2 = srst(s,end)
            if end2==-1:
                return "syx err",-1
            return Par((exp,exp2)),end2
        raise Exception()
    def sdot(s,pos):
        exp,end = sexp(s,pos)
        if end==-1:
            raise SyxErr()
        tag2,end2 = peekToken(s,end)
        if tag2[0]=='wht':
            tag2,end2 = peekToken(s,end2)
        if not tag2[0]=='rpr':
            raise SyxErr("I need ')' please!")
        return exp,end2
        raise Exception()
    def sshr(s,pos):
        exp,end = sexp(s,pos)
        if end==-1:
            raise SyxErr()
        if listp(exp):
            #print exp
            return Vec(sexpToPyList(exp)),end
##        if exp=="t":
##            return True,end
##        elif exp=='f':
##            return False,end
        raise NotImplemented
    return sexp(text,start)
#read = peekSexp#remove later
def eq(x,y):
    return (x is y)
def eqv(x,y):
    return x is y if isinstance(x,Iterable) or isinstance(x,Iterable) else x==y
def equal(x,y):
    return x==y
def check(ture):
    if not ture:
        raise Exception()
    return True
#display==print str(x)
#write==print repr(x)
#read==print eval(x)
assert not eq('1',Sym('1'))
assert not eqv('1',Sym('1'))
assert not equal('1',Sym('1'))
