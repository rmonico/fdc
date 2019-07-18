#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from unittest import TestCase

from di_container.injector import Inject
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

    def test_inject_into_factory_for_external_dependencies(self):
        di_container.load_resources([__package__])

        injected = InjectedWithExternalTransient()

        di_container.inject_resources(injected)

        self.assertTrue(injected._was_set)

    def test_run_before_injection(self):
        di_container.load_resources([__package__])

        injected = InjectedWithCodeRunningBeforeInjection()

        di_container.inject_resources(injected)

        self.assertTrue(injected._before_injection_ran)

    def test_inject_via_attribute(self):
        di_container.load_resources([__package__])

        injected = InjectedViaAttribute()

        di_container.inject_resources(injected)

        self.assertIsInstance(injected._dependency, Dependency)


class Injected(object):

    def __init__(self):
        self._dependency = Inject('dependency_name')


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


class InjectedWithExternalTransient(object):

    def __init__(self):
        self._was_set = None

    def set_dependency_of_external_dependency_was_set(self, was_set):
        self._was_set = was_set


class ExternalDependencyWithTransient(object):

    def __init__(self):
        self._dependency = None

    @staticmethod
    def get_external_resources():
        return [{'name': 'dependency_of_external_dependency_was_set',
                 'creator': ExternalDependencyWithTransient.check_if_dependency_of_external_was_created}]

    def set_transient_dependency(self, dependency):
        self._dependency = dependency

    def check_if_dependency_of_external_was_created(self):
        return self._dependency is not None


class InjectedWithCodeRunningBeforeInjection(object):

    def __init__(self):
        self._before_injection_ran = False

    def before_inject(self):
        self._before_injection_ran = True


class InjectedViaAttribute(object):

    def __init__(self):
        self._dependency = Inject('dependency_name')
