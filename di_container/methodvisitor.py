import inspect


class MethodVisitor(object):
    _classes = []
    _modules = []

    def __init__(self, modules, _filter=lambda: True):
        self._modules = modules
        self._filter = _filter

    def _load_classes(self):
        for module in self._modules:
            if module in MethodVisitor._modules:
                return

            import importlib

            command_module = importlib.import_module(module)

            import pkgutil
            import inspect

            classes = []
            for importer, modulename, ispkg in pkgutil.iter_modules(command_module.__path__):
                submodule = importlib.import_module(
                    "{}.{}".format(module, modulename))
                for class_name, clazz in inspect.getmembers(submodule, predicate=inspect.isclass):
                    if not clazz in classes:
                        classes.append(clazz)

            MethodVisitor._classes += classes
            MethodVisitor._modules += [module]

    def _parent_module_name(self, module):
        module_name = str(module)

        return module_name[:module_name.rfind(".")]

    def _is_at_module(self, clazz):
        clazz_parent_module_name = self._parent_module_name(clazz.__module__)

        for module in self._modules:
            if clazz_parent_module_name.startswith(module):
                return True

        return False

    def visit(self, visitor):
        self._load_classes()

        for clazz in MethodVisitor._classes:
            if self._is_at_module(clazz):
                for method_name, method in inspect.getmembers(clazz, predicate=inspect.isfunction):
                    if self._filter(clazz, method):
                        visitor(clazz, method)
