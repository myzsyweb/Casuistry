#!python27
if 0:
    import sys
    import gc
    sys.setrecursionlimit(2**15-1)
    gc.disable()
else:
    import sys
    import gc
    sys.setrecursionlimit(500)
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
class Err(Exception):
    pass
class Obj:
    pass
nil = None
def cons(car,cdr):
    return Par.cons(car,cdr)
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
    #must no rec here!
def listp(lst):
    raise NotImplementedError()
class T:
    pass
class Char:#not use it,do as python do
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
    def __repr__(self):
        return "(%s . %s)"%(self.car,self.cdr)
    def map(self,pred):
        return Par.cons(pred(self.car),self.cdr.map(pred) if self.cdr else None)
##    def fold(self,pred):
##        return
    def toPyList(self):
        #assert listp(self)
        pair = self
        pyList = []
        while pair:
            pyList.append(pair.car)
            #pyList[-1]=pyList[-1].toPyList() if listp(pyList[-1]) else pyList[-1]
            pair = pair.cdr
        return pyList
    #def __iter__
class Sym(str):
    pass
class Str(str):
    pass
from fractions import Fraction
from numbers import Number
def numberp(x):
    return isa(x,Number)
class Num(Fraction):
    def __repr__(self):
        return str(self)
class Bol:
    pass
class SymMap(dict):
    pass
class Env:
    def __init__(self,var=None,bas=None):
        self.bas = bas
        self.var = var or {}#only Sym allow
    def __repr__(self):
        return str((self.var,self.bas))
    def define(self,sym,val):
        if sym in self.var:
            raise Exception("I has '%s' already."%sym)
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
        while pairp(arg):
            var[car(arg)]=car(val)
            arg,val=map(cdr,(arg,val))
        if not nullp(arg):
            var[arg]=val
        #print "extend>",var
        return Env(var,self)
class Prc:
    def __init__(self,pred=None):
        self.pred = pred
    def apply(self,arg):
        assert pairp(arg) or nullp(arg)
        if self.pred:
            return self.pred(arg)
        else:
            raise NotImplementedError
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
            return Str(tag[1][1:-1]),end
        elif tag[0]=='qte':
            exp,end = sexp(s,end)
            if end==-1:
                return "syx err",-1
            return Par((Sym("quote"),Par.cons(exp,None))),end
        elif tag[0]=='lpr':
            exp,end = srst(s,end)
            if end==-1:
                return "syx err",-1
            return (exp),end
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
    return sexp(text,start)
read = peekSexp

def check(ture):
    if not ture:
        raise Exception()

