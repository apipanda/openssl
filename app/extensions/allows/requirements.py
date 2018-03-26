import operator
from abc import ABCMeta, abstractmethod
from flask._compat import with_metaclass


class Requirement(with_metaclass(ABCMeta)):

    @abstractmethod
    def fulfill(self, user, request):
        return NotImplemented

    def __call__(self, user, request):
        return self.fulfill(user, request)

    def __repr__(self):
        return '<{}()>'.format(self.__class__.__name__)


class ConditionalRequirement(Requirement):
    def __init__(self, *requirements, **kwargs):
        self.requirements = requirements
        self.op = kwargs.get('op', operator.and_)
        self.until = kwargs.get('until')
        self.negated = kwargs.get('negated')

    @classmethod
    def And(cls, *requirements):
        return cls(*requirements, op=operator.and_, until=False)

    @classmethod
    def Or(cls, *requirements):
        return cls(*requirements, op=operator.or_, until=True)

    @classmethod
    def Not(cls, *requirements):
        return cls(*requirements, negated=True)

    def fulfill(self, user, request):
        reduced = None
        for r in self.requirements:
            result = r(user, request)

            if reduced is None:
                reduced = result
            else:
                reduced = self.op(reduced, result)

            if self.until == reduced:
                break

        if reduced is not None:
            return not reduced if self.negated else reduced

        return False

    def __and__(self, require):
        return self.And(self, require)

    def __or__(self, require):
        return self.Or(self, require)

    def __invert__(self):
        return self.Not(self)

    def __repr__(self):
        additional = []

        for name in ['op', 'negated', 'until']:
            value = getattr(self, name)
            if not value:
                continue
            additional.append('{0}={1!r}'.format(name, value))

        if additional:
            additional = ' {}'.format(', '.join(additional))
        else:
            additional = ''

        return "<{0} requirements={1!r}{2}>".format(self.__class__.__name__,
                                                    self.requirements,
                                                    additional)


(C, And, Or, Not) = (ConditionalRequirement, ConditionalRequirement.And,
                     ConditionalRequirement.Or, ConditionalRequirement.Not)
