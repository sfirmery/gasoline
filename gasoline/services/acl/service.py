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
        logger.debug('check %r with acl %r', permission, acl)
        if isinstance(acl, Container) and len(acl) < 0:
            return
        thruth = self.get_thruth(permission, current_user, acl)
        if thruth == 'ALLOW':
            logger.debug('ALLOW for space')
            return
        elif thruth == 'DENY':
            logger.debug('DENY for space')
            abort(403,
                  _('You are not allowed to "%(permission)s" this\
 %(resource)s',
                    permission=PERMISSIONS.get(permission, _('unknown')),
                    resource=resource))
        else:
            logger.debug('no match for space, ignore')
            return

    def can(self, permission, acl):
        """return whether user can do action or not"""
        logger.debug('check %r with acl %r', permission, acl)
        if isinstance(acl, Container) and len(acl) < 0:
            return True
        thruth = self.get_thruth(permission, current_user, acl)
        if thruth == 'ALLOW':
            return True
        elif thruth == 'DENY':
            return False
        else:
            return True

    def acl(self, permission, *args, **kwargs):
        from gasoline.models import Space

        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if 'space' in kwargs:
                    space = Space.objects(name=kwargs.get('space')).first()
                    if space is not None:
                        acl = space.acl
                    resource = _('space')
                if acl:
                    self.apply(permission, space.acl, resource)
                return f(*args, **kwargs)

            return wrapped
        return decorator

    @classmethod
    def get_thruth(cls, permission, user, acl):
        """get thruth value from acl for permission and user"""
        logger.debug('get thruth for permission %r for user %r with acl %r',
                     permission, user, acl)
        match = []
        for ace in acl:
            predicate_match = cls.check_predicate(ace.predicate, current_user)
            perm_match = cls.check_permission(ace.permission, permission)
            if predicate_match and perm_match:
                match.append(ace.truth)
        if len(match) > 0:
            if 'DENY' in match:
                return 'DENY'
            else:
                return match[0]
        else:
            return None

    @classmethod
    def check_predicate(cls, predicate, user):
        logger.debug('check predicate %r with %r', predicate, user)
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
            if predicate == user.name:
                return True
        else:
            return False

    @classmethod
    def check_permission(cls, perms, req_perm):
        logger.debug('check perm %r with %r', perms, req_perm)
        if isinstance(perms, Container):
            return req_perm in perms
        else:
            raise TypeError('permissions must be a container')
