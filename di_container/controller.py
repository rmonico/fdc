#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .methodvisitor import MethodVisitor
from .injector import di_container


class Controller(object):

    def __init__(self):
        self._listeners = []

    def set_logger(self, logger):
        self._logger = logger

    def _get_instance_for(self, clazz):
        for listener, instance in self._listeners:
            if instance and instance.__class__ == clazz:
                return instance

        return clazz()

    def _load_listeners_from(self, clazz, method):
        instance = self._get_instance_for(clazz)

        self._listeners.append({'listener': getattr(instance, method.__name__), 'instance': instance})

    def load_listeners(self, packages):
        visitor = MethodVisitor(packages, lambda clazz, method: method.__name__.endswith('_handler'))

        visitor.visit(self._load_listeners_from)

        di_container.inject_resources(self)

        for listener in self._listeners:
            self._logger.info('Loaded listener: {}', listener[0].__qualname__)

    def event(self, event_name, *args, **kwargs):
        for listener, instance in self._listeners:
            if listener.__name__ == (event_name + '_handler'):
                listener(*args, **kwargs)

controller = Controller()
