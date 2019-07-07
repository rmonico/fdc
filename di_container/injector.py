#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .methodvisitor import MethodVisitor


class Injector(object):

    def __init__(self):
        self._resource_classes = []

    def set_logger(self, logger):
        self._logger = logger

    def load_resource(self, clazz, method):
        resource_name = method()

        resource_properties = {'name': resource_name, 'class': clazz, 'instance': None}

        self._resource_classes.append(resource_properties)

    def load_resources(self, package):
        visitor = MethodVisitor(package, lambda method_name, method: method_name == 'injectable_resource')

        visitor.visit(self.load_resource)

        self.inject_resources(self)

        for resource in self._resource_classes:
            self._logger.info('Loaded resource: {name} (of {class})', **resource)

    def inject_resources(self, client):
        for properties in self._resource_classes:
            injection_method_name = 'set_' + properties['name']

            if (not hasattr(client, injection_method_name)):
                continue

            injection_method = getattr(client, injection_method_name)

            instance = properties['instance']

            if not instance:
                instance = properties['instance'] = properties['class']()

            injection_method(instance)

di_container = Injector()
