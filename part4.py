from part3 import *
def symbolp(sexp):
    return isa(sexp,str)
def pp(sexp):
    if sexp is None:
        return "'()"
    elif sexp==True:
        return "#t"
    elif sexp==False:
        return "#f"
    #elif eofp(sexp)
    elif symbolp(sexp):
        return "%s"%str(sexp).upper()
    #stringp(sexp) '""'%sexp uns***
    elif procedurep(sexp):
        return "<procedure>"
    elif pairp(sexp):
        if listp(sexp):
            return "[%s]"%(" ".join(pp(x) for x in sexp.toPyList()))
        else:
            return "(%s . %s)"%map(pp,(sexp.car,sexp.cdr))
    else:
        return str(sexp)
def displayToStr():
    pass
##def writeToStr():
##    pass
