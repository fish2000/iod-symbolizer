#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from collections import defaultdict, namedtuple

def autoincrementer():
    """ Get an independantly auto-incrementing unary function """
    def inc():
        """ Get a uniquely auto-incremented integer value """
        if not hasattr(inc, 'v'):
            setattr(inc,    'v', 0)
        out = getattr(inc,  'v')
        setattr(inc,        'v', out + 1)
        return out
    return inc

class AutoInc(object):
    # Get a uniquely auto-incremented integer value
    __slots__ = ('v',)
    
    def __init__(self, value=0):
        try:
            # assume we got another AutoInc ...
            # ... I could sure use SFINAE right about now
            self.v = value.v
        except AttributeError:
            self.v = int(value)
    
    def __call__(self):
        self.v += 1
        return self.v
    
    def add(self, value):
        self.v += int(value)
    
    def __int__(self):
        return self.v
    def __float__(self):
        return float(self.v)
    def __long__(self):
        return long(self.v)
    
    def __repr__(self):
        return str(self.v)

class Histogram(defaultdict):
    
    @staticmethod
    def lexcmp(k0, k1):
        """ Hacky comparator to privilege string length """
        return cmp(len(k1), len(k0)) or cmp(k0, k1)
    
    @staticmethod
    def autoinc():
        return AutoInc()
    
    def __init__(self, *args, **kwargs):
        if len(args) and not len(kwargs):
            for arg in args:
                argcls_name = arg.__class__.__name__
                if argcls_name.startswith('FrozenHistogram'):
                    # reconstitute FrozenHistogram
                    kwargs.update(arg._asdict())
                else:
                    # normal arg: column name
                    kwargs.update({ arg: AutoInc() })
        super(Histogram, self).__init__(
            Histogram.autoinc, *tuple(), **kwargs)
    
    def prettyprint(self, **kwargs):
        from pprint import pformat
        return "%s%s" % (
            self.__class__.__name__,
            pformat((Histogram.autoinc, dict(self)), **kwargs))
    
    def __repr__(self):
        return self.prettyprint()
    
    def __str__(self):
        longest_key = sorted(self.iterkeys(), cmp=Histogram.lexcmp)
        return self.prettyprint(
            depth=10,
            width=len(longest_key)/2)
    
    ### SET LOGIC ###
    def setresult(self, keyset):
        pass
    
    def __and__(self, rhs):
        """ & (intersection) """
        pass
    
    def __or__(self, rhs):
        """ | (union) """
        pass
    
    def __xor__(self, rhs):
        """ ^ (symmetric difference) """
        pass
    
    def __sub__(self, rhs):
        """ - (difference [NON-COMMUTATIVE!]) """
        pass
    
    def inc(self, idx):
        return self[str(idx)]()
    
    def add(self, idx, value):
        return self[str(idx)].add(value)
    
    def keyset_hash(self):
        return hex(abs(hash(self.iterkeys())))
    
    def frozentype(self, rename=True):
        return namedtuple('FrozenHistogram_%s' % self.keyset_hash(),
            tuple(self.iterkeys()), rename=rename)
    
    def freeze(self):
        return self.frozentype()(**dict(
            (ituple[0], int(ituple[1])) for ituple in self.iteritems()
        ))
    
    def normalize(self):
        ceil = float(sum(int(v) for v in self.itervalues()))
        return self.frozentype()(**dict(
            (ituple[0], float(ituple[1]) / ceil) for ituple in self.iteritems()
        ))
    
    def max(self):
        return max(*(int(v) for v in self.values()))
    def min(self):
        return min(*(int(v) for v in self.values()))

