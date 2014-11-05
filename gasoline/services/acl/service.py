# -*- coding: utf-8 -*-
""""""

import logging
from collections import Container
from functools import wraps
from flask import abort
from flask.ext.login import current_user
from flask.ext.babel import gettext as _, lazy_gettext as _l

from gasoline.services.base import Service

__all__ = ['ACLService']

logger = logging.getLogger('gasoline')

PERMISSIONS = {
    'read': _l('read'),
    'write': _l('write'),
    'delete': _l('delete'),
    'write.comments': _l('write comments'),
    'write.attachments': _l('write attachments'),
}


class ACLService(Service):
    name = 'acl'

    def init_app(self, app):
        """intialise ACL service with flask configuration"""
        super(ACLService, self).init_app(app)

    def apply(self, permission, acl, resource=_l('resource')):
        """apply acl, abort if not allowed"""
        logger.info('check %r with acl %r', permission, acl)
        if isinstance(acl, Container) and len(acl) < 0:
            return
        truth = self.get_truth(permission, current_user, acl)
        if truth == 'ALLOW':
            logger.info('ALLOW for {}'.format(resource))
            return
        elif truth == 'DENY':
            logger.info('DENY for {}'.format(resource))
            abort(403,
                  _('You are not allowed to "%(permission)s" this\
 %(resource)s',
                    permission=PERMISSIONS.get(permission, _('unknown')),
                    resource=resource))
        else:
            logger.info('no match for {}, ignore'.format(resource))
            return

    def can(self, permission, acl):
        """Return whether user can do action or not"""
        logger.info('check %r with acl %r', permission, acl)
        if isinstance(acl, Container) and len(acl) < 0:
            return True
        truth = self.get_truth(permission, current_user, acl)
        if truth == 'ALLOW':
            return True
        elif truth == 'DENY':
            return False
        else:
            return True

    def acl(self, permission, *args, **kwargs):
        """A decorator that is used to apply the global and space acl before the request"""
        from gasoline.models import Space

        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                acl = None
                if 'space' in kwargs:
                    space = Space.objects(name=kwargs.get('space')).first()
                    if space is not None:
                        acl = space.acl
                    resource = _('space')
                if acl:
                    self.apply(permission, acl, resource)
                return f(*args, **kwargs)

            return wrapped
        return decorator

    @classmethod
    def get_truth(cls, permission, user, acl):
        """get truth value from acl for permission and user"""
        logger.info('get truth for permission %r for user %r with acl %r',
                     permission, user, acl)
        match = []
        for ace in acl:
            predicate_match = cls.check_predicate(ace.predicate, current_user)
            perm = cls.get_permission(ace.truth, permission)
            if predicate_match:
                match.extend(perm)
        if len(match) > 0:
            if 'DENY' in match:
                return 'DENY'
            else:
                return 'ALLOW'
        else:
            return None

    @classmethod
    def check_predicate(cls, predicate, user):
        logger.info('check predicate %r with %r', predicate, user)
        if predicate == 'ANY':
            return True
        elif predicate == 'OWNER':
            # TODO: check resource owner
            return False
        elif predicate.startswith('g:'):
            predicate = predicate[2:]
            # TODO: check on user's groups
            return False
        elif predicate.startswith('u:'):
            predicate = predicate[2:]
            if hasattr(user, 'name') and predicate == user.name:
                return True
        else:
            return False

    @classmethod
    def get_permission(cls, perms, req_perm):
        logger.info('get perm %r in %r', req_perm, perms)
        try:
            return [perm for perm in perms if req_perm in perm]
        except:
            raise TypeError('permissions not found')
