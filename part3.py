from part2 import *
##toplevel9 = None
##def inEnv():
##    return toplevel
#print "####part2################"
class TypErr(Exception):
    pass
##def peekSexp(code):
##    return read(code)
##def read1(code):
##    return read(code)[0]
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

def block(f):
    return f()
@block
def globalMacro():
    def defmacro(code):#not use outside,dut to scope
        sexp = Scm.read(code)
        #print ">",Scm.read(code)
        assert sexp.car=='defmarco'
        name = sexp.cdr.car
        marco_rule = cons('lambda',sexp.cdr.cdr)
        #trans = Scm.eval(marco_rule,Scm().env())
        def expend(sexp):
            trans = Scm.eval(marco_rule,topenvrn)#here?
            #print topenvrn.var.keys()
            #print 'list' in topenvrn.var.keys()
            #print sexp
            expended_code = trans.apply(sexp.cdr)
            #print ">>>>>>>",expended_code
            return buildExp9(expended_code)
        topmacro[name] = expend
    defmacro("""(defmarco define lst
                 (if (pair? (car lst))
                     (cons '::define (cons (car (car lst)) (cons (cons 'lambda (cons (cdr (car lst)) (cdr lst))) '())))
                     (cons '::define lst))))""")
    defmacro("""(defmarco begin lst
                    (cons '::begin lst))""")

    defmacro("""(defmarco cond (h . t)
                  (if (eq? (car h) 'else)
                      (if (null? t)
                          (cons 'begin (cdr h))
                          (error "ELSE isn't last"))
                      (list 'if (car h)
                            (cons 'begin (cdr h))
                            (cons 'cond t))))""")
    #why not use define?
    defmacro("""(defmarco case lst 
              (define expand-rest-case (lambda (lst)
              (if (null? lst)
                  (list 'quote '())
                  (if (eq? (car (car lst)) 'else)
                      (if (null? (cdr lst))
                          (cons 'begin (cdr (car lst)))
                          (error "ELSE isn't last"))
                      (list 'if (list 'member ':: (list 'quote (car (car lst))))
                            (cons 'begin (cdr (car lst)))
                            (expand-rest-case (cdr lst)))))))
            (list (list 'lambda '(::) (expand-rest-case (cdr lst)))(car lst)))""")
    defmacro("""(defmarco let lst
            (apply 
             (lambda (name bind . stmt)
               (list (list 'lambda (list)(cons 'define (cons (cons name (map car bind)) stmt))
                           (cons name (map cadr bind)))))
             (if (pair? (car lst)) (cons ':: lst) lst)))""")
    
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
    def defun(name,env=None):
            env = env if env else topenvrn
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
            @defun("apply1",env)#with cont
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
##            @defun("-",env)
##            def _(x):
##                    return x.car-x.cdr.car
    topenvrn.define("+",Prc(lambda arg:reduce(lambda x,y:x+y,arg.toPyList() if arg else [],0)))
    topenvrn.define("-",Prc(lambda arg:reduce(lambda x,y:x-y,arg.toPyList())))
    topenvrn.define("*",Prc(lambda arg:reduce(lambda x,y:x*y,arg.toPyList()if arg else [],1)))
    topenvrn.define("/",Prc(lambda arg:reduce(lambda x,y:x/y,arg.toPyList())))
    topenvrn.define("pair?",Prc(lambda arg:pairp(arg.car)))
    bindPyFunc(topenvrn,"null?",nullp)
    bindPyFunc(topenvrn,"number?",numberp)
    topenvrn.define("not",Prc(lambda arg:not arg.car))
    topenvrn.define("apply",BlkApp9())
    eval9(Scm.read("""1"""),topenvrn)
    if 0:
        eval9(Scm.read("""(begin
            (define list (lambda x x))
            (define cdar (lambda (x) (cdr (car x))))
            (define cadr (lambda (x) (car (cdr x))))
            )"""),topenvrn)
    with open("initlib.scm") as f:
        #libCode = "(::begin %s)"%f.read()
        code = f.read()
        s = 0
        while 1:
            t,s = peekSexp(code,s)
            if s==-1:
                break
            eval9(t,topenvrn)  
            print ">>",t
        #eval9(Scm.read(libCode),topenvrn)       

    topenvrn.define("#t",True)
    topenvrn.define("#f",False)#use lex later

##    Scm.eval(Scm.read("""
##    (define (append . x)
##      (define (append a b)
##            (if (null? a) b
##                    (cons (car a) (append (cdr a) b))))
##      (fold-left append '() x))
##    """),topenvrn)
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
