from .allows import _allows, _make_callable


class Permission(object):

    def __init__(self, *requirements, **opts):
        self.ext = _allows._get_current_object()
        self.requirements = requirements
        self.throws = opts.get('throws', self.ext.throws)
        self.identity = opts.get('identity')
        self.on_fail = _make_callable(opts.get('on_fail', self.ext.on_fail))

    def __bool__(self):
        return self.ext.fulfill(self.requirements, identity=self.identity)

    __nonzero__ = __bool__

    def __enter__(self):
        if not self:
            self.on_fail()
            raise self.throws

    def __exit__(self, exctype, value, tb):
        pass
