#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .classvisitor import ClassVisitor, has_method, has_function


class Injector(object):

    def __init__(self):
        self._resource_classes = []

    def set_logger(self, logger):
        self._logger = logger

    def load_resource(self, injectable_class):
        resource_name = injectable_class.injectable_resource()

        resource_properties = {'name': resource_name, 'class': injectable_class, 'instance': None}

        self._resource_classes.append(resource_properties)

    def load_resources(self, package):
        visitor = ClassVisitor(package, lambda clazz: has_function(clazz, 'injectable_resource'))

        visitor.visit(self.load_resource)

        self.inject_resources(self)

        for resource in self._resource_classes:
            self._logger.info('Loaded resource: {name} (of {class})', **resource)

    def inject_resources(self, client):
        for properties in self._resource_classes:
            injection_method_name = 'set_' + properties['name']

            if (not has_method(client, injection_method_name)):
                continue

            injection_method = getattr(client, injection_method_name)

            instance = properties['instance']

            if not instance:
                instance = properties['instance'] = properties['class']()

            injection_method(instance)


injector = Injector()
