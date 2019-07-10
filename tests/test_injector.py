#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from unittest import TestCase

from di_container.injector import di_container


class InjectorTestCase(TestCase):

    def test_internal_dependency_injection(self):
        di_container.load_resources([__package__])

        injected = Injected()

        di_container.inject_resources(injected)

        self.assertIsInstance(injected._dependency, Dependency)

    def test_external_dependency_injection(self):
        di_container.load_resources([__package__])

        injected = InjectedExternal()

        di_container.inject_resources(injected)

        self.assertEqual(injected._external_dependency, 'external dependency instance')

    def test_transient_dependency_injection(self):
        di_container.load_resources([__package__])

        injected = InjectedTransient()

        di_container.inject_resources(injected)

        self.assertIsInstance(injected._dependency_with_transient._transient_dependency, TransientDependency)


class Injected(object):

    def __init__(self):
        self._dependency = None

    def set_dependency_name(self, dependency):
        self._dependency = dependency


class Dependency(object):

    @staticmethod
    def injectable_resource():
        return 'dependency_name'


class InjectedExternal(object):

    def __init__(self):
        self._external_dependency = None

    def set_external_dependency(self, dependency):
        self._external_dependency = dependency


class ExternalDependency(object):

    @staticmethod
    def get_external_resources():
        return [{'name': 'external_dependency',
                 'creator_factory': ExternalDependency,
                 'creator': ExternalDependency.callable_who_will_return_dependency_instance_when_injected}]

    def callable_who_will_return_dependency_instance_when_injected(self):
        return 'external dependency instance'


class InjectedTransient(object):

    def __init__(self):
        self._dependency_with_transient = None

    def set_dependency_with_transient(self, dependency):
        self._dependency_with_transient = dependency


class DependencyWithTransient(object):

    def __init__(self):
        self._transient_dependency = None

    def set_transient_dependency(self, dependency):
        self._transient_dependency = dependency

    @staticmethod
    def injectable_resource():
        return 'dependency_with_transient'


class TransientDependency(object):

    @staticmethod
    def injectable_resource():
        return 'transient_dependency'
