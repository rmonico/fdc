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

    def test_should_trow_exception_when_unexisting_dependency_is_found(self):
        di_container.load_resources([__package__])

        injected = InjectNotExistingDependency()

        with self.assertRaises(Exception) as context:
            di_container.inject_resources(injected)

        self.assertIsInstance(context.exception, Exception)
        self.assertEqual('Dependency not found: "dependency which doesnt exists"', str(context.exception))

    def test_should_throw_exception_when_unexisting_dependency_is_get(self):
        with self.assertRaises(Exception) as context:
            di_container.get_resource('dependency which doesnt exists')

        self.assertIsInstance(context.exception, Exception)
        self.assertEqual('Dependency not found: "dependency which doesnt exists"', str(context.exception))

    def test_should_call_di_container_error_handler_when_unexisting_dependency_is_get(self):
        di_container.load_resources


class Injected(object):

    def __init__(self):
        self._dependency = Inject('dependency_name')


class Dependency(object):

    @staticmethod
    def injectable_resource():
        return 'dependency_name'


class InjectedExternal(object):

    def __init__(self):
        self._external_dependency = Inject('external_dependency')


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
        self._dependency_with_transient = Inject('dependency_with_transient')


class DependencyWithTransient(object):

    def __init__(self):
        self._transient_dependency = Inject('transient_dependency')

    @staticmethod
    def injectable_resource():
        return 'dependency_with_transient'


class TransientDependency(object):

    @staticmethod
    def injectable_resource():
        return 'transient_dependency'


class InjectedWithExternalTransient(object):

    def __init__(self):
        self._was_set = Inject('dependency_of_external_dependency_was_set')


class ExternalDependencyWithTransient(object):

    def __init__(self):
        self._dependency = Inject('transient_dependency')

    @staticmethod
    def get_external_resources():
        return [{'name': 'dependency_of_external_dependency_was_set',
                 'creator': ExternalDependencyWithTransient.check_if_dependency_of_external_was_created}]

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


class InjectNotExistingDependency(object):

    def __init__(self):
        self._dependency = Inject('dependency which doesnt exists')


@DependencyNotFoundObserver(filter='^dependency which doesnt exists$')
class DependencyWhichDoesntExistNotFoundObserver(object):

    def handle(self, dependency_name):
        return 'system exit'
