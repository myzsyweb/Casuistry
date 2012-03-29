__all__=['isa','nullp',]
isa=isinstance
def nullp(obj):
    return obj is None
def pairp(pair):
    return isa(pair,Pair)
from collections import Iterable
from abc import ABCMeta,abstractproperty
class Pair(Iterable):
    __metaclass__ = ABCMeta
    @abstractproperty
    def car(self):
        pass
    @abstractproperty
    def cdr(self):
        pass
    def __iter__(self):
        def iter(self):
            while pairp(self):
                yield self.car
                self = self.cdr
            assert nullp(self)
        return iter(self)
class Immutable:
    __metaclass__ = ABCMeta
class DottedPair:
    pass
##class Seq(Pair):
##    def __init__(self,iterator):
##        self.ready = False
##        self.iter = iterator
##    def force(self):
##        if self.ready:
##            return
##        try:
##            self._car = next(self.iter)
##            self._cdr = Seq(self.iter)
##        except StopIteration:
##            pass
##        self.ready=True
##    @staticmethod
##    def fromIter(lst):
##        return Seq(iter(lst))
##    @property
##    def car(self):
##        self.force()
##        return self._car
##    @property
##    def cdr(self):
##        self.force()
##        return self._cdr
##    @property
##    def nullp(self):
##        return False
##a=Seq.fromIter(xrange(3))
##print a.car
##print a.car
##print a.cdr.car
##print a.cdr.cdr.car
##print a.cdr.cdr.cdr
class Stream(Pair):
    def __init__(self,head,tail):
        self._car=head
        self._iter=tail
        self._ready=False
    @staticmethod
    def fromIter(lst):
        it=iter(lst)
        try:
            return Stream(next(it),it)
        except StopIteration:
            return None
    @property
    def car(self):
        return self._car
    @property
    def cdr(self):
        if not self._ready:
            try:
                self._cdr = Stream(next(self._iter),self._iter)
            except StopIteration:
                self._cdr = None
            self._ready=True
        return self._cdr
a=Stream.fromIter(xrange(3))
print a.car
print a.car
print a.cdr.car
print a.cdr.cdr.car
print a.cdr.cdr.cdr
