# This code is part of Grandalf
# Copyright (C) 2008-2015 Axel Tillequin (bdcht3@gmail.com) and others
# published under GPLv2 license or EPLv1 license
# Contributor(s): Axel Tillequin

from collections import OrderedDict

import sys
_IS_PY2 = sys.version_info[0] == 2

#------------------------------------------------------------------------------
# Poset class implements a set but allows to interate over the elements in a
# deterministic way and to get specific objects in the set.
# Membership operator defaults to comparing __hash__  of objects but Poset
# allows to check for __cmp__/__eq__ membership by using contains__cmp__(obj)
class  Poset(object):

    def __init__(self, L=()):
        self.o = OrderedDict()
        self._unordered = set()
        for obj in L:
            self.add(obj)

    def __repr__(self):
        return 'Poset(%r)' % (self.o,)

    def __str__(self):
        f = '%%%dd' % len(str(len(self.o)))
        s = []
        for i, x in enumerate(self.o.values()):
            s.append(f % i + '.| %s' % repr(x))
        return '\n'.join(s)
    
    def add(self, obj):
        if obj in self._unordered:
            return self.get(obj)
        else:
            self.o[obj] = obj
            self._unordered.add(obj)
            return obj

    def remove(self, obj):
        if obj in self._unordered:
            obj = self.get(obj)
            self._unordered.discard(obj)
            del self.o[obj]
            return obj
        return None

    def index(self, obj):
        return list(self).index(obj)

    def get(self, obj):
        return self.o.get(obj, None)

    def __getitem__(self, i):
        return list(self)[i]

    def __len__(self):
        return len(self.o)

    def __iter__(self):
        if _IS_PY2:
            return self.o.itervalues()
        else:
            return iter(self.o.values())

    def __cmp__(self, other):
        return cmp(self._unordered, other._unordered)

    def __eq__(self, other):
        return self._unordered == other._unordered

    def __ne__(self, other):
        return not self == other

    def copy(self):
        return Poset(self)

    __copy__ = copy
    def deepcopy(self):
        from copy import deepcopy
        L = deepcopy(self.o.values())
        return Poset(L)

    def __or__(self, other):
        return self.union(other)

    def union(self, other):
        p = Poset(self)
        p.update(other)
        return p

    def update(self, other):
        self.o.update(other.o)
        self._unordered.update(other._unordered)

    def __and__(self, other):
        s1 = self._unordered
        s2 = other._unordered
        return Poset(s1.intersection(s2))

    def intersection(self, *args):
        p = self
        for other in args:
            p = p & other
        return p

    def __xor__(self, other):
        s1 = self._unordered
        s2 = other._unordered
        return Poset(s1.symmetric_difference(s2))

    def symmetric_difference(self, *args):
        p = self
        for other in args:
            p = p ^ other
        return p

    def __sub__(self, other):
        s1 = self._unordered
        s2 = other._unordered
        return Poset(s1.difference(s2))

    def difference(self, *args):
        p = self
        for other in args:
            p = p - other
        return p

    def __contains__(self, obj):
        return obj in self._unordered

    def contains__cmp__(self, obj):
        return obj in self._unordered

    def issubset(self, other):
        s1 = self._unordered
        s2 = other._unordered
        return s1.issubset(s2)

    def issuperset(self, other):
        s1 = self._unordered
        s2 = other._unordered
        return s1.issuperset(s2)

    __le__ = issubset
    __ge__ = issuperset

    def __lt__(self, other):
        return (self <= other and len(self) != len(other))

    def __gt__(self, other):
        return (self >= other and len(self) != len(other))
