#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from unittest import TestCase

from di_container.injector import di_container


class InjectorTestCase(TestCase):

    def test_internal_dependency_injection(self):
        di_container.load_resources([__package__])

        injected = Injected()

        di_container.inject_resources(injected)

        self.assertIsInstance(injected._dependency, DependencyToBeInjected)


class Injected(object):

    def set_dependency_name(self, dependency):
        self._dependency = dependency


class DependencyToBeInjected(object):

    def injectable_resource():
        return 'dependency_name'
