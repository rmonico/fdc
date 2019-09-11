from .methodvisitor import MethodVisitor


class Inject(object):

    def __init__(self, name):
        self.dependency_name = name


class Injector(object):

    def __init__(self):
        self._resource_classes = []
        self._logger = None

    def load_resources(self, packages):
        self._load_internal_resources(packages)
        self._load_external_resources(packages)

        self._logger = self.get_resource('logger', optional=True)

        if self._logger:
            for resource in self._resource_classes:
                self._logger.info('Loaded resource: {name} (of {creator})'.format(**resource))

    def load_resources_from_class(self, *classes):
        for cls in classes:
            self._load_resources_from_class(cls)

    def _load_resources_from_class(self, cls):
        method = getattr(cls, 'injectable_resource', None)

        if method:
            self._load_internal_resource(cls, method)
            return

        method = getattr(cls, 'get_external_resources', None)

        if method:
            self._load_external_resource(cls, method)
            return

        raise InjectorException('Class "{}" has no resources to load'.format(cls.__name__))

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
        if self._logger:
            self._logger.debug('Injecting resources into "{}"', client)

        import inspect

        if hasattr(client, 'before_inject'):
            if inspect.ismethod(getattr(client, 'before_inject')):
                client.before_inject()

        if not hasattr(client, '__dict__'):
            return

        for attribute, value in client.__dict__.items():
            if not isinstance(value, Inject):
                continue

            dependency = self._get_dependency_by_name(value.dependency_name)

            self.inject_resources(dependency)

            client.__dict__[attribute] = dependency

    def get_resource(self, resource_name, optional=False):
        for properties in self._resource_classes:
            if properties['name'] == resource_name:
                instance = self._get_instance(properties)
                self.inject_resources(instance)
                return instance

        if not optional:
            raise Exception('Dependency not found: "{}"'.format(resource_name))

    def _get_dependency_by_name(self, dependency_name):
        dependency_found = False

        for dependency in self._resource_classes:
            if dependency['name'] == dependency_name:
                return self._get_instance(dependency)

        if not dependency_found:
            raise Exception('Dependency not found: "{}"'.format(dependency_name))

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


class InjectorException(Exception):
    pass


di_container = Injector()

