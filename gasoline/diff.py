# -*- coding: utf-8 -*-

from diff_match_patch import diff_match_patch


class Diff(diff_match_patch):
    """Diff"""

    def __init__(self):
        diff_match_patch.__init__(self)
