#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .methodvisitor import MethodVisitor


class Injector(object):

    def __init__(self):
        self._resource_classes = []
        self._logger = None

    def set_logger(self, logger):
        self._logger = logger

    def load_resources(self, packages):
        self._load_internal_resources(packages)
        self._load_external_resources(packages)

        self.inject_resources(self)

        for resource in self._resource_classes:
            if self._logger:
                self._logger.info('Loaded resource: {name} (of {creator})', **resource)

    def _load_internal_resources(self, packages):
        visitor = MethodVisitor(packages, lambda clazz, method: method.__name__ == 'injectable_resource')
        visitor.visit(self._load_internal_resource)

    def _load_internal_resource(self, clazz, method):
        resource_name = method()

        resource_properties = {'name': resource_name, 'creator': clazz, 'instance': None}

        self._resource_classes.append(resource_properties)

    def _load_external_resources(self, packages):
        visitor = MethodVisitor(packages, lambda clazz, method: method.__name__ == 'get_external_resources')
        visitor.visit(self._load_external_resource)

    def _load_external_resource(self, clazz, method):
        resources = method()

        for resource in resources:
            resource.setdefault('instance', None)

        self._resource_classes += resources

    def inject_resources(self, client):
        for properties in self._resource_classes:
            injection_method_name = 'set_' + properties['name']

            if not hasattr(client, injection_method_name):
                continue

            injection_method = getattr(client, injection_method_name)

            instance = properties['instance']

            if not instance:
                instance = properties['instance'] = properties['creator']()

            injection_method(instance)


di_container = Injector()
