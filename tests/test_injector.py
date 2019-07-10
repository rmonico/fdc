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

        injected = Injected()

        di_container.inject_resources(injected)

        self.assertEqual(injected._external_dependency, 'external dependency instance')


class Injected(object):

    def __init__(self):
        self._dependency = None

    def set_dependency_name(self, dependency):
        self._dependency = dependency


class Dependency(object):

    @staticmethod
    def injectable_resource():
        return 'dependency_name'

    @staticmethod
    def get_external_resources():
        return [{'name': 'external_dependency',
                 'creator': DependencyToBeInjected.callable_who_will_return_dependency_instance_when_injected}]

        @staticmethod
        def callable_who_will_return_dependency_instance_when_injected():
            return 'external dependency instance'
