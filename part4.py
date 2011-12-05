from part3 import *
def pprint(sexp):
    if sexp==None:
        return "'()"
    elif sexp==True:
        return "#t"
    elif sexp==False:
        return "#f"
    #elif eofp(sexp)
    elif symbolp(sexp):
        return "<symbol %s>"%sexp
    #stringp(sexp) '""'%sexp uns***
    elif procedurep(sexp):
        return "<procedure>"
    elif pair(sexp):
        if listp(sexp):
            return str(pprint(x) for x in sexp.toPyList())
        else:
            return "(%s . %s)"%map(pprint,(sexp.car,sexp.cdr))
    else:
        return sexp
