#!python2.7
import sys
sys.setrecursionlimit(2**15-1)
import gc
gc.disable()
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
#def parsec(string)
##s=seq("(",or(num,str),")")
#num=
#str=


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
code_calc24="""
((lambda ()
(define (reverse l)
  (if (null? l) '()
     (append (reverse (cdr l)) (list (car l)))))
(define (calc24 a b c d)
  (define (flat-map p x)
    (apply append (map p x)))
  (define (filter p x)
    (cond ((null? x) '())
          ((p (car x)) (cons (car x) (filter p (cdr x))))
          (else (filter p (cdr x)))))
  (define (drop-one x lst)
    (cond ((null? lst) '())
          ((equal? x (car lst)) (cdr lst))
          (else (cons (car lst) (drop-one x (cdr lst))))))
  (define (perm lst)
    (if (null? lst)
        '(())
        (flat-map 
         (lambda (x)
           (map (lambda (y) (cons x y))
                (perm (drop-one x lst))))
         lst)))
  (define (pow lst n)
    (if (zero? n) '(())
        (flat-map
         (lambda (x)
           (map (lambda (y) (cons x y))
                (pow lst (- n 1))))
         lst)))
  (define (buld-exp num ops)
    (apply
     (lambda (i j k l)
       (apply 
        (lambda (o p q)
          (list
           (list o (list p i j) (list q k l))
           (list o (list p i (list q j k)) l)))
        ops))
     num))
  (define (eval-exp exp)
    (if (pair? exp)
        (let ((arg (map eval-exp (cdr exp)))
              (/ (lambda (x y)
                   (if (zero? y) +nan.0 (/ x y)))))
          (case (car exp)
            ((+) (apply + arg))
            ((-) (apply - arg))
            ((*) (apply * arg))
            ((/) (apply / arg))
            ((--) (apply - (reverse arg)))
            ((//) (apply / (reverse arg)))
            (else (error "op?"))))
        exp))
  (define (show-exp exp)
    (define (bin-op-str op arg)
      (apply (lambda (x y)
               (string-append "(" x op y ")"))
             (map (lambda (x) 
                    (if (number? x) (number->string x) x)) arg)))
    (if (pair? exp)
        (let ((arg (map show-exp (cdr exp)))
              (/ (lambda (x y) (if (zero? y) +nan.0 (/ x y)))))
          (case (car exp)
            ((+) (bin-op-str "+" arg))
            ((-) (bin-op-str "-" arg))
            ((*) (bin-op-str "*" arg))
            ((/) (bin-op-str "/" arg))
            ((--) (bin-op-str "-" (reverse arg)))
            ((//) (bin-op-str "/" (reverse arg)))
            (else (error "op?"))))
        exp))
  (define (unique lst)
    (if (null? lst) '()
        (cons (car lst) 
              (unique 
               (filter (lambda (x)
                         (not (equal? x (car lst)))) lst)))))
  (unique
   (flat-map 
    (lambda (x)
      (flat-map
       (lambda (y)
         (flat-map
          (lambda (z)
            (if (= 24 (eval-exp z))
                (let ((show (show-exp z)))
                  (display show)
                  (list show))
                '())) 
          (buld-exp x y)))
       (pow '(+ - * / -- //) 3))) 
    (perm (list a b c d)))))
(display "start")
(newline)
(calc24 2 3 8 9)
(newline)   
(display "finish")  
))
"""
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
def listp(lst):
    pass
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
class Env:
    def __init__(self,var=None,bas=None):
        self.bas = bas
        self.var = var or {}#only Sym allow
    def __repr__(self):
        return str((self.var,self.bas))
    def define(self,sym,val):
        if sym in self.var:
            raise Exception()
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
class Lmd(Prc):
    def __init__(self,lmd,env):
        self.lmd = lmd
        self.arg = lmd.cdr.car
        self.bdy = lmd.cdr.cdr#!!!
        self.env = env
    @staticmethod
    def make(arg,bdy,env):
        return 
    def __repr__(self):
        return str(('LAMBDA',self.lmd,'env'))
    def apply(self,arg):#move the method to a func?
        #print "body>",self.bdy
        rt = self.env.extend(self.arg,arg)#entend env here!!!
        return self.bdy.map(lambda x:eval(x,rt)).toPyList()[-1]
        #fold-left
        #return eval(self.bdy,self.env.extend(self.arg,arg))  
#########################yacc####################
class Reader:
    pass
class SyxErr(Exception):
    pass
class Eof:
    pass
def read(text):
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
    return sexp(text,0)
print read(code)
print read("(+ a b c)")
#######################runtime#############
class Exp:
    def __call__(self,env,cont=None):
        pass
    def do(self):
        pass
class Blk:
    def __init__(self,proc):
        self.proc=proc
    def __call__(self,env,cont=None):
        self.proc(env)
    def do(self):
        pass
class Ret:
    pass
class Cont:
    pass
class Ret:
    pass
def runSexp(cc):
    while not isa(cc,Ret):
        cc = cc.run()
    else:
        return cc.val()
class BlkLmd(Prc):
    def __init__(self,arg,blk,env):
        self.arg = arg
        self.bdy = blk
        self.env = env
    def __repr__(self):
        return 'LAMBDA '+object.__repr__()
    def apply(self,arg):
        rt = self.env.extend(self.arg,arg)#entend env here!!!
        return self.bdy.map(lambda x:x(rt)).toPyList()[-1]
def buildExp(sexp):
    def form(sexp):
        assert pairp(sexp)
        op = car(sexp)
        if op==Sym('if'):
            test = build(sexp.cdr.car)#eval(sexp.cdr.car,env)
            then = build(sexp.cdr.cdr.car)
            fail = build(sexp.cdr.cdr.cdr.car)
            return lambda env:then(env)if test(env) else fail(env)
        elif op==Sym('lambda'):
            #body = build(sexp.cdr.cdr)
            body = sexp.cdr.cdr.map(build)
            return lambda env:BlkLmd(sexp.cdr.car, body ,env)
        elif op==Sym('define'):
            val = build(sexp.cdr.cdr.car)
            return lambda env:env.define(sexp.cdr.car,val(env))
        elif op==Sym('quote'):
            val = sexp.cdr.car
            return lambda env:val
        raise Exception()
    def build(sexp):
        if pairp(sexp):
            if car(sexp) in [Sym('if'),Sym('lambda'),Sym('quote'),Sym('define')]:
                return form(sexp)
            op = build(car(sexp))
            arg = sexp.cdr.map(build) if sexp.cdr else None
            return lambda env:op(env).apply(arg.map(lambda exp:exp(env)) if arg else None)
        #op.apply(sexp.cdr.map(lambda x:eval(x,env)) if sexp.cdr else None)
        elif isa(sexp,Sym):
            return lambda env:env.lookup(sexp)
        else:
            return lambda env:sexp
    return build(sexp)
def eval2(sexp,env):
    return buildExp(sexp)(env)
#=====================================try=======================
####let Blk return pair (cont,ret)
##class BlkLmd2(Prc):
##    def __init__(self,arg,blk,env):
##        self.arg = arg
##        self.bdy = blk
##        self.env = env
##    def __repr__(self):
##        return 'LAMBDA '+object.__repr__()
##    def apply(self,arg):
##        rt = self.env.extend(self.arg,arg)#entend env here!!!
##        return self.bdy.map(lambda x:x(rt,lambda y:y)).toPyList()[-1]#######do sth here#######do sth here
##        #t=[0]
##        #def ret(v):
##        #    t[0] = v
##        #reduce(lambda s,i:i(rt,s),self.bdy.toPyList(),ret)
##        #return t[0]
##        #ret b1 b2 b3
##        #b3(e,b2(e,b1(e,ret)))
##        #(lambda () (a) (b) 1)
##        #b3(e,b2(e,b1(e,c)))
##        #self.bdy:list<blk>
##        #analyze-sequence
##        """
##        (define (analyze-sequence exps)
##          (define (sequentially a b)
##            (lambda (env succeed fail)
##              (a env
##                 ;; success continuation for calling a
##                 (lambda (a-value fail2)
##                   (b env succeed fail2))
##                 ;; failure continuation for calling a
##                 fail)))
##          (define (loop first-proc rest-procs)
##            (if (null? rest-procs)
##                first-proc
##                (loop (sequentially first-proc (car rest-procs))
##                      (cdr rest-procs))))
##          (let ((procs (map analyze exps)))
##            (if (null? procs)
##                (error "Empty sequence -- ANALYZE"))
##            (loop (car procs) (cdr procs))))
##        """
##def buildExp2(sexp):
##    def form(sexp):
##        assert pairp(sexp)
##        op = car(sexp)
##        if op==Sym('if'):
##            test = build(sexp.cdr.car)
##            then = build(sexp.cdr.cdr.car)
##            fail = build(sexp.cdr.cdr.cdr.car)
##            return lambda env,c:c(then(env)if test(env) else fail(env))
##        elif op==Sym('lambda'):
##            body = build(sexp.cdr.cdr)
##            return lambda env,c:c(BlkLmd2(sexp.cdr.car, body ,env))
##        elif op==Sym('define'):
##            val = build(sexp.cdr.cdr.car)
##            return lambda env,c:c(env.define(sexp.cdr.car,val(env)))
##        elif op==Sym('quote'):
##            val = sexp.cdr.car
##            return lambda env,c:c(val)
##        raise Exception()
##    def build(sexp):
##        if pairp(sexp):
##            if car(sexp) in [Sym('if'),Sym('lambda'),Sym('quote'),Sym('define')]:
##                return form(sexp)
##            op = build(car(sexp))
##            arg = sexp.cdr.map(build)#######do sth here#######do sth here
##            #reduce(lambda s,i:i(rt,s),self.bdy.toPyList(),ret)
##            #get-args
##            #analyze-application
##            t=[0]
##            def ret(val):
##                t[0]=val
##            return lambda env,c:c(op(env,ret).apply(arg.map(lambda exp:exp(env))))
##        #op.apply(sexp.cdr.map(lambda x:eval(x,env)) if sexp.cdr else None)
##        elif isa(sexp,Sym):
##            return lambda env,c:c(env.lookup(sexp))
##        else:
##            return lambda env,c:c(sexp)
##    return build(sexp)
##def eval3(sexp,env):
##    t=[0]
##    def ret(val):
##        t[0]=val
##    buildExp2(sexp)(env,ret)
##    return t[0]
#===============here
##let Blk return pair (cont,ret)
class BlkLmd3(Prc):
    def __init__(self,arg,blk,env):
        self.arg = arg
        self.bdy = blk
        self.env = env
    def __repr__(self):
        return 'LAMBDA '+object.__repr__()
    def apply(self,arg):
        rt = self.env.extend(self.arg,arg)#entend env here!!!
        return self.bdy.map(lambda blk:blk(rt,lambda y:y)).toPyList()[-1]#######do sth here#######do sth here
        #t=[0]
        #def ret(v):
        #    t[0] = v
        #reduce(lambda s,i:i(rt,s),self.bdy.toPyList(),ret)
        #return t[0]
        #ret b1 b2 b3
        #b3(e,b2(e,b1(e,ret)))
        #(lambda () (a) (b) 1)
        #b3(e,b2(e,b1(e,c)))
        #self.bdy:list<blk>
        #analyze-sequence
        """
        (define (analyze-sequence exps)
          (define (sequentially a b)
            (lambda (env succeed fail)
              (a env
                 ;; success continuation for calling a
                 (lambda (a-value fail2)
                   (b env succeed fail2))
                 ;; failure continuation for calling a
                 fail)))
          (define (loop first-proc rest-procs)
            (if (null? rest-procs)
                first-proc
                (loop (sequentially first-proc (car rest-procs))
                      (cdr rest-procs))))
          (let ((procs (map analyze exps)))
            (if (null? procs)
                (error "Empty sequence -- ANALYZE"))
            (loop (car procs) (cdr procs))))
        """
class Cont:
    pass
class BlkLmd4(Prc):
    def __init__(self,arg,blk,env):
        self.arg = arg
        self.bdy = blk
        self.env = env
    def __repr__(self):
        return 'LAMBDA '+object.__repr__()
    def apply(self,arg):
        rt = self.env.extend(self.arg,arg)
        t=["err"]
        def ret(val):
            t[0] = val
        self.bdy(rt,ret)(None)
        return t[0]
    def apply2(self,arg,cont):
        rt = self.env.extend(self.arg,arg)
        return self.bdy(rt,cont)(None)
def buildExp3(sexp):
    def form(sexp):
        assert pairp(sexp)
        op = car(sexp)
        if op==Sym('if'):
            test = build(sexp.cdr.car)
            then = build(sexp.cdr.cdr.car)
            fail = build(sexp.cdr.cdr.cdr.car)
            #return lambda env,c:c(then(env)if test(env) else fail(env))
            return lambda env,c:test(env,lambda v:then(env,c)if v else fail(env,c))
        elif op==Sym('lambda'):
            arg = sexp.cdr.car
            bodys = sexp.cdr.cdr.map(build)#to one blk
            #[blk1,blk2,blk3,blk4]
            #body = reduce(lambda s,i:build(s,lambda v:),sexp.cdr.cdr.toPyList(),ret)
            #bodyw = lambda env,c:c(bodys.map(lambda blk:blk(env,lambda y:y)).toPyList()[-1])
            bodyq = lambda env,c:reduce(lambda cont,blk:(lambda v:blk(env,cont)),reversed(bodys.toPyList()),c)
            #[blk4,blk3,blk2,blk1]c ->blk3(e,(lambda v:blk4(e,c))
            #lambda env,c:blk1(env,lambda v:blk2(env,lambda v:lastblk(env,c)))
            return lambda env,c:c(BlkLmd4(arg, bodyq ,env))
        elif op==Sym('define'):
            name = sexp.cdr.car
            val = build(sexp.cdr.cdr.car)
            #return lambda env,c:c(env.define(sexp.cdr.car,val(env)))
            return lambda env,c:c(val(env,lambda v:c(env.define(name,v))))
        elif op==Sym('quote'):
            val = sexp.cdr.car
            return lambda env,c:c(val)
        raise Exception()
    def build(sexp):
        if pairp(sexp):
            if car(sexp) in [Sym('if'),Sym('lambda'),Sym('quote'),Sym('define')]:
                return form(sexp)
            op = build(car(sexp))
            arg = sexp.cdr.map(build) if sexp.cdr else None#######do sth here#######do sth here
            #reduce(lambda s,i:i(rt,s),self.bdy.toPyList(),ret)
            #get-args
            #lambda v
            #blk1(env,lambda v:cons(v,bl2(env,lambda v:)))
            def get_args(arg,env,cont):
                #arg:[blk1,blk2mlk3...blkn]
                #return lambda env,c:blk1(end,lambda v:cons(v,blk2(env,lambda v:cons(v,blkn(env,c)))
                #bodyq = lambda env,c:reduce(lambda cont,blk:lambda v1:blk(env,lambda v2:cons(v1,v2)),reversed(bodys.toPyList()),c)
                if nullp(arg):
                    return cont(nil)
                else:
                    car(arg)(env,lambda v1:get_args(arg.cdr,env,lambda v2:cont(cons(v1,v2))))
            #reduce(lambda cont,blk: blk(env,lambda v:) ,arg)
            def app(obj,arg,cont):
                if isa(obj,BlkLmd4):
                    return obj.apply2(arg,cont)
                else:
                    return cont(obj.apply(arg))
            return lambda env,c:op(env,lambda v1:get_args(arg,env,lambda v2:app(v1,v2,c)))
            #analyze-application
            return lambda env,c:c(op(env,lambda op:op.apply(arg.map(lambda blk:blk(env,lambda y:y))if arg else None)))
        #op.apply(sexp.cdr.map(lambda x:eval(x,env)) if sexp.cdr else None)
        elif isa(sexp,Sym):
            return lambda env,c:c(env.lookup(sexp))
        else:
            return lambda env,c:c(sexp)
    return build(sexp)
def eval4(sexp,env):
    t=[0]
    def ret(val):
        #print ">",val
        t[0] = val
    buildExp3(sexp)(env,ret)
    return t[0]                            
###################eval##########################
#@button("I'm sure!")
#def submit(self):pass
sform = []
smacro = [Sym('define'),Sym('begin'),Sym('cond'),Sym('let'),Sym('case')]#hash later
def macro(sexp,env):
    #DEFMACRO
    #defmacro
    assert pairp(sexp)
    op = car(sexp)
    if op==Sym('define'):
        #print "macro>",sexp.toPyList() #list(sexp)
        marco_rule="""
            (lambda (lst)
                  (if (pair? (car lst))
                      (list '::define (car (car lst)) (cons 'lambda (cons (cdar lst) (cdr lst))))
                      (cons '::define lst)))
            """
        trans = eval(read(marco_rule)[0],toplevel)#get a lambda
        expended_code = trans.apply(Par.cons(sexp.cdr,nil))
        return eval(expended_code,env)
    elif op==Sym('begin'):
        marco_rule="""(lambda (lst) (list (cons 'lambda (cons '() lst))))"""
        trans = eval(read(marco_rule)[0],toplevel)#get a lambda
        expended_code = trans.apply(Par.cons(sexp.cdr,nil))
        return eval(expended_code,env)
    elif op==Sym('let'):
        marco_rule="""
          (lambda (lst)
            (apply 
             (lambda (name bind . stmt)
               (list (list 'lambda (list)(cons 'define (cons (cons name (map car bind)) stmt))
                           (cons name (map cadr bind)))))
             (if (pair? (car lst)) (cons ':: lst) lst)))
            """
        trans = eval(read(marco_rule)[0],toplevel)#get a lambda
        expended_code = trans.apply(Par.cons(sexp.cdr,nil))
        #raise Exception(expended_code.toPyList())
        return eval(expended_code,env)
        """
        (let loop ((x 1)(y 2))
        (+ x y))
        ;->
        ((lambda ()
        (define (loop x y)
        (+ x y))
        (loop 1 2)
        ))
        """
    elif op==Sym('cond'):
        marco_rule="""
            ((lambda ()
              (define (expand-cond lst)
                (if (null? lst)
                    (list 'quote '())
                    (if (eq? (car (car lst)) 'else)
                        (if (null? (cdr lst))
                            (cons 'begin (cdr (car lst)))
                            (error "ELSE isn't last"))
                        (list 'if (car (car lst))
                              (cons 'begin (cdr (car lst)))
                              (expand-cond (cdr lst))))))
              expand-cond))
            """
        trans = eval(read(marco_rule)[0],toplevel)#get a lambda
        expended_code = trans.apply(Par.cons(sexp.cdr,nil))
        return eval(expended_code,env)
    elif op==Sym('case'):
        marco_rule="""
          (lambda (lst)
            (define (expand-rest-case lst)
              (if (null? lst)
                  (list 'quote '())
                  (if (eq? (car (car lst)) 'else)
                      (if (null? (cdr lst))
                          (cons 'begin (cdr (car lst)))
                          (error "ELSE isn't last"))
                      (list 'if (list 'member ':: (list 'quote (car (car lst))))
                            (cons 'begin (cdr (car lst)))
                            (expand-rest-case (cdr lst))))))
            (list (list 'lambda '(::) (expand-rest-case (cdr lst)))(car lst)))
            """
        trans = eval(read(marco_rule)[0],toplevel)#get a lambda
        expended_code = trans.apply(Par.cons(sexp.cdr,nil))
        return eval(expended_code,env)
    raise Exception()
def form(sexp,env):
    assert pairp(sexp)
    op = car(sexp)
    if op==Sym('if'):
        test = eval(sexp.cdr.car,env)
        if test:
            return eval(sexp.cdr.cdr.car,env)
        else:
            return eval(sexp.cdr.cdr.cdr.car,env)
    elif op==Sym('lambda'):
        return Lmd(sexp,env)
    elif op==Sym('::define'):
        env.define(sexp.cdr.car,eval(sexp.cdr.cdr.car,env))
        return None
    elif op==Sym('quote'):
        return sexp.cdr.car
    elif op==Sym('+'):#!!!remove later
        return sum(map(lambda x:eval(x,env),sexpToPyList(cdr(sexp)))) 
    elif op==Sym('what'):
        raise NotImplementedError()
    raise Exception()
def eval(sexp,env):
    if pairp(sexp):
        if car(sexp) in [Sym('if'),Sym('lambda'),Sym('quote'),Sym('::define')]:
            return form(sexp,env)
        if car(sexp) in smacro:
            return macro(sexp,env)
        op = eval(car(sexp),env)
        if isa(op,Prc):#let apply throws exception,remove 'if'
            return op.apply(sexp.cdr.map(lambda x:eval(x,env)) if sexp.cdr else None)
        else:
            raise Exception(type(sexp),sexp)
    elif isa(sexp,Sym):
        return env.lookup(sexp)
    else:
        return sexp
############################toplevel#####################
#from functools import partial
def build(*arg,**kw):
    return lambda f:f(*arg,**kw)
def bldr(f):
    return f()
def genv():
    return toplevel
def check(ture):
    if not ture:
        raise Exception()
toplevel = Env()
def defun(name,env):
    return lambda f:env.define(Sym(name),Prc(f))
def bindPyFunc(env,name,proc):
    return env.define(name,Prc(lambda arg:apply(proc,arg.toPyList())))

@build(toplevel)
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
toplevel.define("+",Prc(lambda arg:reduce(lambda x,y:x+y,arg.toPyList() if arg else [],0)))
#toplevel.define("-",Prc(lambda arg:reduce(lambda x,y:x-y,arg.toPyList())))
toplevel.define("*",Prc(lambda arg:reduce(lambda x,y:x*y,arg.toPyList()if arg else [],1)))
toplevel.define("/",Prc(lambda arg:reduce(lambda x,y:x/y,arg.toPyList())))
toplevel.define("pair?",Prc(lambda arg:pairp(arg.car)))
#toplevel.define("null?",Prc(lambda arg:nullp(arg.car)))
bindPyFunc(toplevel,"null?",nullp)
bindPyFunc(toplevel,"number?",numberp)
#toplevel.define("number?",Prc(lambda arg:numberp(arg.car)))
#toplevel.define("number?",Prc(lambda arg:numberp(arg.car)))
toplevel.define("not",Prc(lambda arg:not arg.car))
toplevel.define("list",Lmd(read('(lambda x x)')[0],toplevel))
toplevel.define("cdar",Lmd(read('(lambda (x) (cdr (car x)))')[0],toplevel))
toplevel.define("cadr",Lmd(read('(lambda (x) (car (cdr x)))')[0],toplevel))
toplevel.define("#t",True)
toplevel.define("#f",False)#use lex later
eval(read("""
(define (fold-right p i x)
  (if (null? x) i
      (p (car x) (fold-right p i (cdr x)))))
""")[0],toplevel)
eval(read("""
(define (fold-left p i x)
  (if (null? x) i
      (fold-left p (p i (car x)) (cdr x))))
""")[0],toplevel)
eval(read("""(define (map f x) (fold-right (lambda (a b) (cons (f a) b)) '() x))""")[0],toplevel)
eval(read("""
(define (append . x) 
  (define (append a b)
    (if (null? a) b
        (cons (car a) (append (cdr a) b))))
  (fold-left append '() x))
""")[0],toplevel)
eval(read("""
(define (member obj lst)
  (cond
    ((null? lst) #f)
    ((equal? obj (car lst)) lst)
    (else (member  obj (cdr lst)))))
""")[0],toplevel)
eval(read("""
(define (zero? n) (= n 0))
""")[0],toplevel)
@bldr
def defineString():
    @defun("::string-append",toplevel)
    def _(x):
        check(isa(x.car,str))
        check(isa(x.cdr.car,str))
        return x.car+x.cdr.car
    eval(read("""(define (string-append . x) (fold-left ::string-append "" x))""")[0],toplevel)
@bldr
def defineType():
    @defun("number->string",toplevel)
    def _(x):
        check(numberp(x.car))
        return str(x.car)
##eval(read("""(define (append . x)
##(define (append a b)
##
##)
##(fold-right (lambda (a b) (cons (f a) b)) '() x))""")[0],toplevel)
#toplevel.define(">",Prc(lambda arg:reduce(lambda x,y:x>y,arg.toPyList())))
#toplevel.define("<",Prc(lambda arg:reduce(lambda x,y:x<y,arg.toPyList())))

#print read("((lambda x (apply + x)) 1 58)")[0
#print eval(read("((lambda x (apply + x)) 1 58)")[0],Env())
#############conti###############
#######################repl#################
class S:
##    def __init__(self):
##        self.env = toplevel.extend()
    @staticmethod
    def read(text):
        return read(text)[0]
##    @staticmethod
##    def eval(sexp,env):
##        return eval(sexp,env)
class Repl():
    pass
def repl():
    env = toplevel.extend()
    while True:
        #try:
        print eval(S.read(raw_input('scm> ')),env)
        #except Exception as e:
        #print e
        
##############test##########################
import unittest
class Test(unittest.TestCase):
    def test_env(self):
        a = Env()
        b = a.extend()
        a.define("a",1)
        self.assertTrue(b.lookup("a")==1)
        b.define("a",2)
        self.assertTrue(a.lookup("a")==1)
        self.assertTrue(b.lookup("a")==2)
    def test_read(self):
        self.assertEqual(len(read("(+ 1 4)")[0].toPyList()),3)
    def test_calc(self):
        self.assertEqual( eval(read("(+ 1 6)")[0],toplevel.extend()) ,7)
        self.assertTrue( isa(eval(read("(lambda (x) (+ x 1))")[0],toplevel.extend()),Prc))
        self.assertEqual(eval(read("(display 1)")[0],toplevel.extend()),None)
        self.assertEqual( eval(read("((lambda (x) (+ x 1)) 7 )")[0],toplevel.extend()) ,8)
        self.assertEqual( eval(read("((lambda (x y) (+ x y)) 1 9)")[0],toplevel.extend()) ,10)
        self.assertEqual( eval(read("((lambda () (define x 1) (+ x 2)))")[0],toplevel.extend()) ,3)
        self.assertEqual( eval(read("((lambda () (define x 1) (if (> 1 2) x (+ x 6))))")[0],toplevel.extend()) ,7)
    def test_frac(self):
        code = """
            ((lambda ()
                (define fac
                  (lambda (x)
                    (if (> x 0) 
                        (* x (fac (- x 1)))
                        1)))
                (fac 6)))
        """
        self.assertEqual( eval(read(code)[0],toplevel.extend()) ,720)
    def test_pair(self):
        self.assertTrue( nullp(read("'a")[0].cdr.cdr))
        self.assertTrue( nullp(read("'(a)")[0].cdr.car.cdr))
        self.assertEqual(eval(read("(car (cdr '(1 . (2 3))))")[0],toplevel.extend()),2)
        self.assertEqual(eval(read("(cdr '(1 . 2))")[0],toplevel.extend()),2)
        self.assertEqual(len(read("'(1 2 3 ))")[0].toPyList()),2)
        self.assertEqual(len(eval(read("'(1 2 3 ))")[0],toplevel.extend()).toPyList()),3)
    def test_apply(self):
        self.assertEqual( eval(read("((lambda (x) (+ (car x) (car (cdr x)))) '(1 2))")[0],toplevel.extend()) ,3)
        self.assertEqual( eval(read("((lambda x (+ (car x) (car (cdr x)))) 1 2)")[0],toplevel.extend()) ,3)
        self.assertEqual( eval(read("(apply + '(1 2))")[0],toplevel.extend()) ,3)
        self.assertEqual( eval(read("(apply (lambda (x . y) (+ x (car y))) '(1 2))")[0],toplevel.extend()) ,3)
    def test_macro1(self):
        code = """((lambda ()
                    (define (fac x)
                        (if (> x 0) 
                            (* x (fac (- x 1)))
                            1))
                    (fac 6)
                    ))"""
        self.assertEqual( eval(read(code)[0],toplevel.extend()) ,720)
    def test_macro2(self):
        self.assertEqual( eval(read("""((lambda ()
                    (cond
                    ((= 1 2) 3)
                    (else 4))
                    ))""")[0],toplevel.extend()) ,4)
        self.assertEqual( eval(read("""((lambda ()
                    (case (+ 1 1)
                    ((1) 1)
                    ((2) 2))
                    ))""")[0],toplevel.extend()) ,2)
        self.assertEqual( eval(read("""((lambda ()(let loop ((x 10))(if (< x 0) 0 (+ x (loop (- x 1)))))))""")[0],toplevel.extend()) ,55)
        self.assertEqual( eval(read("""(begin (define x 1) x)""")[0],toplevel.extend()) ,1)
    def test_macro3(self):
        pass
    def test_builtin(self):
        self.assertEqual( eval(read("(apply + (map (lambda (x) (+ x 1)) '(0 1 2 3 4)))")[0],toplevel.extend()) ,15)
        self.assertEqual( eval(read("""(string-append)""")[0],toplevel.extend()) ,"")
        self.assertEqual( eval(read("""(string-append "ab" "cd")""")[0],toplevel.extend()) ,"abcd")
        self.assertEqual( eval(read("""(string-append "ab" "cd" "ef")""")[0],toplevel.extend()) ,"abcdef")
        self.assertEqual( eval(read("""(string-append "a" (number->string 1))""")[0],toplevel.extend()) ,"a1")
        self.assertTrue( eval(read("(= 1 1)")[0],toplevel.extend()))
        self.assertTrue(not eval(read("(eqv? 'a 'b)")[0],toplevel.extend()))
        self.assertTrue( eval(read("(eqv? 'a 'a)")[0],toplevel.extend()))
        self.assertTrue( eval(read("(eqv? '(1 2) '(1 2))")[0],toplevel.extend()))
        self.assertTrue( nullp(eval(read("(append)")[0],toplevel.extend())))
        self.assertEqual( len(eval(read("(append '(1 2) '(3 4 5) '(6) '(7 8))")[0],toplevel.extend()).toPyList()),8)
        self.assertTrue( eval(read("""(pair? '(1 2))""")[0],toplevel.extend()))
        self.assertTrue(not eval(read("""(pair? 1)""")[0],toplevel.extend()))
        self.assertEqual( eval(read("""(cadr (member 2 '(1 2 3)))""")[0],toplevel.extend()) ,3)
        self.assertTrue(not eval(read("""(member 4 '(1 2 3))""")[0],toplevel.extend()))
    def test_calc24(self):
        #print eval(read(code_calc24)[0],toplevel.extend())
        pass
if __name__ == '__main__':
    pass
    #repl()
    #unittest.main()
print read("(+ 1 8)")
print eval(read("(list 1 2 3)")[0],toplevel.extend())
print eval(read("""((lambda ()
(define (f x) x)
(f 1)
))""")[0],toplevel.extend())
print eval(read("(+ 1 2)")[0],toplevel.extend())
print eval2(read("(+ 1 2)")[0],toplevel.extend())
print eval2(read("(list 1 2 3)")[0],toplevel.extend())
print eval(read("(*)")[0],toplevel.extend())
print eval2(read("(*)")[0],toplevel.extend())
print eval4(read("(*)")[0],toplevel.extend())
print eval(read("((lambda (x) (+ x 1)) 7 )")[0],toplevel.extend())
print eval2(read("((lambda (x) (+ x 1)) 7 )")[0],toplevel.extend())
print eval4(read("((lambda (x) (+ x 1)) 7 )")[0],toplevel.extend())
print eval4(read("(+ 1 2)")[0],toplevel.extend())
print eval4(read("(list 1 2 3)")[0],toplevel.extend())
print eval4(read("1")[0],toplevel.extend())
print eval4(read("*")[0],toplevel.extend())
print eval2(read("""((lambda () (display "a") (display "b") (display "c") "d" 12121212))""")[0],toplevel.extend())
print eval4(read("""((lambda () (display "a") (display "b") (display "c") "d" 343434))""")[0],toplevel.extend())
print eval4(read("""121212""")[0],toplevel.extend())
