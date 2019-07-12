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

        resource_properties = {'name': resource_name, 'factory': None, 'creator': clazz, 'instance': None}

        self._resource_classes.append(resource_properties)

    def _load_external_resources(self, packages):
        visitor = MethodVisitor(packages, lambda clazz, method: method.__name__ == 'get_external_resources')
        visitor.visit(self._load_external_resource)

    def _load_external_resource(self, clazz, method):
        resources = method()

        for resource in resources:
            resource.setdefault('instance', None)
            resource.setdefault('factory', clazz)

        self._resource_classes += resources

    def inject_resources(self, client):
        import inspect

        if hasattr(client, 'before_inject'):
            if inspect.ismethod(getattr(client, 'before_inject')):
                client.before_inject()

        for properties in self._resource_classes:
            injection_method_name = 'set_' + properties['name']

            if not hasattr(client, injection_method_name):
                continue

            injection_method = getattr(client, injection_method_name)

            instance = self._get_instance(properties)

            self.inject_resources(instance)

            injection_method(instance)

    def get_resource(self, resource_name):
        for properties in self._resource_classes:
            if properties['name'] == resource_name:
                return self._get_instance(properties)

    def _get_instance(self, properties):
        instance = properties['instance']

        if not instance:
            if properties['factory']:
                factory = properties['factory']()

                self.inject_resources(factory)

                instance = properties['instance'] = properties['creator'](factory)
            else:
                instance = properties['instance'] = properties['creator']()

        return instance


di_container = Injector()
