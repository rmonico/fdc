#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .classvisitor import ClassVisitor, has_method, has_function


class Controller(object):

    def load_listeners(self, package):
        print('TODO')

    def event(self, event_name, *args, **kwargs):
        print('TODO')

controller = Controller()
