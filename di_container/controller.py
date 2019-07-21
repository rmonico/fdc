from .injector import di_container
from .methodvisitor import MethodVisitor
from .injector import Inject


class ControllerEventResult(object):

    def __init__(self, status, data=None, kwdata=None):
        self.status = status
        self.data = data
        self.kwdata = kwdata


class Controller(object):

    def __init__(self):
        self._listeners = []
        self._logger = Inject('logger')

    def _get_instance_for(self, clazz):
        for listener, instance in self._listeners:
            if instance and instance.__class__ == clazz:
                return instance

        instance = clazz()

        di_container.inject_resources(instance)

        return instance

    def _load_listeners_from(self, clazz, method):
        instance = self._get_instance_for(clazz)

        attribute = getattr(instance, method.__name__)

        if not self._is_already_loaded(attribute, instance):
            self._listeners.append((attribute, instance))

    def _is_already_loaded(self, attribute, instance_to_be_loaded):
        for listener, instance in self._listeners:
            if listener == attribute and instance == instance_to_be_loaded:
                return True

        return False

    def load_listeners(self, packages):
        visitor = MethodVisitor(packages, lambda clazz, method: method.__name__.endswith('_handler'))

        visitor.visit(self._load_listeners_from)

        di_container.inject_resources(self)

        for listener in self._listeners:
            self._logger.info('Loaded listener: {}', listener[0].__qualname__)

    def event(self, event_name, *args, **kwargs):
        self._logger.info('Running {} with args "{}" and kwargs "{}"', event_name, args, kwargs)

        results = []
        for listener, instance in self._listeners:
            if listener.__name__ == (event_name + '_handler'):
                raw_result = listener(*args, **kwargs)

                if isinstance(raw_result, tuple):
                    status = raw_result[0]
                    if isinstance(raw_result[1], dict):
                        kwdata = raw_result[1]
                        data = raw_result[2:]
                    else:
                        kwdata = {}
                        data = raw_result[1:]
                else:
                    status = raw_result
                    data = []
                    kwdata = {}

                results += [ControllerEventResult(status, data, kwdata)]

        return results


controller = Controller()
