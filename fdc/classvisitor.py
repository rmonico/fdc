#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def has_method(clazz, method_name):
    import inspect
    return hasattr(clazz, method_name) and inspect.isfunction(getattr(clazz, method_name))


class ClassVisitor(object):

    _classes = []
    _modules = []

    def __init__(self, module, filter=lambda clazz: True):
        self._module = module
        self._filter = filter

    def _load_classes(self):
        if self._module in ClassVisitor._modules:
            return

        import importlib

        command_module = importlib.import_module(self._module)

        import pkgutil
        import inspect

        classes = []
        for importer, modulename, ispkg in pkgutil.iter_modules(command_module.__path__):
            submodule = importlib.import_module(
                "{}.{}".format(self._module, modulename))
            for class_name, clazz in inspect.getmembers(submodule, predicate=inspect.isclass):
                for method_name, method in inspect.getmembers(clazz, predicate=inspect.isfunction):
                    classes.append(clazz)
                    break

        ClassVisitor._classes += classes
        ClassVisitor._modules += [self._module]

    def _parent_module_name(self, module):
        module_name = str(module)

        return module_name[:module_name.rfind(".")]

    def _is_at_module(self, clazz):
        clazz_parent_module_name = self._parent_module_name(clazz.__module__)

        # TODO Create a flag to disable for submodules
        return clazz_parent_module_name.startswith(self._module)

    def visit(self, visitor):
        self._load_classes()

        for clazz in ClassVisitor._classes:
            if self._is_at_module(clazz):
                if self._filter(clazz):
                    visitor(clazz)
