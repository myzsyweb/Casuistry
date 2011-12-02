#!python27
import sys
import gc
import getopt
from part3 import Scm

__all__ = ['Scm']

scm = Scm()
def repl():
    print "<Casuistry Scheme>  Nov.2011~"
    print "A Simple Scheme Language Implementation Using Python"
    return scm.repl()
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:g")
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-r":
            if a=='max':
                sys.setrecursionlimit(2**15-1)
            elif a=='min':
                sys.setrecursionlimit(200)
            else:
                sys.setrecursionlimit(int(a))
        if o == "-g":
            gc.disable()
    if args:
        sys.setrecursionlimit(2**15-1)
        print Scm.load(args[0],scm.env())
    else:
        print repl()
if __name__ == "__main__":
    main()
