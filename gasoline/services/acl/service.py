# -*- coding: utf-8 -*-
""""""

from collections import Container, Callable
from flask.ext.login import current_user

from gasoline.services.base import Service

__all__ = ['ACLService']


class ACLService(Service):
    name = 'acl'

    def init_app(self, app):
        """intialise ACL service with flask configuration"""
        super(ACLService, self).init_app(app)

    def can(self, permission, **kwargs):
        """check if user can do something"""
        print 'kwargs: %r' % kwargs
        space = kwargs.pop('space', None)
        if space is not None:
            print '(space.acl %r, permission %r)' % (space.acl, permission)
            if self.check(space.acl, permission):
                return True
        return False

    @classmethod
    def check(cls, acl, permission):
        print 'check for acl %r and permission %r' % (acl, permission)
        for ace in acl:
            print 'enter ace %r' % ace
            # predicate_match = current_user == ace.predicate
            # predicate_match = True
            predicate_match = cls.check_predicate(ace.predicate, current_user)
            print 'predicate_match %r' % predicate_match
            perm_match = cls.check_permission(ace.permission, permission)
            print 'perm_match %r' % perm_match
            if predicate_match and perm_match:
                return ace.truth

    @classmethod
    def check_predicate(cls, predicate, user):
        if predicate == 'ANY':
            return True
        if user == predicate:
            return True
        return False

# def parse_predicate(input):
#     if isinstance(input, basestring):
#         negate = input.startswith('!')
#         if negate:
#             input = input[1:]
#         predicate = current_auth.predicates.get(input)
#         if not predicate:
#             raise ValueError('unknown predicate: %r' % input)
#         if negate:
#             predicate = Not(predicate)
#         return predicate
#     if isinstance(input, (tuple, list)):
#         return And(parse_predicate(x) for x in input)
#     return input
#     def predicate(self, name, predicate=None):
#         if predicate is None:
#             return functools.partial(self.predicate, name)
#         self.predicates[name] = predicate
#         return predicate

    @classmethod
    def check_permission(cls, perms, req_perm):
        print 'check perm %r with %r' % (perms, req_perm)
        print 'check type: %r' % type(perms)
        if isinstance(perms, basestring):
            print 'perm string'
            return req_perm == perms
        elif isinstance(perms, Container):
            print 'perm container'
            return req_perm in perms
        elif isinstance(perms, Callable):
            return perms(req_perm)
        else:
            raise TypeError('permission set must be a string, container, or callable')
