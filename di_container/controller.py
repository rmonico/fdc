#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .methodvisitor import MethodVisitor


class Controller(object):

    def __init__(self):
        self._listeners = []

    def _get_instance_for(self, clazz, method):
        for listener, instance in self._listeners:
            if instance and instance.__class__ == clazz:
                return instance

        return clazz()

    def _load_listeners_from(self, clazz, method):
        instance = self._get_instance_for(clazz, method)

        self._listeners.append({'listener': getattr(instance, method.__name__), 'instance': instance})

    def load_listeners(self, package):
        visitor = MethodVisitor(package, lambda clazz, method: method.__name__.endswith('_handler'))

        visitor.visit(lambda method: self._load_listeners_from(method))

    def event(self, event_name, *args, **kwargs):
        for listener, instance in self._listeners:
            listener(instance, args, kwargs)

controller = Controller()
