#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def has_method(clazz, method_name):
    import inspect
    return hasattr(clazz, method_name) and inspect.isfunction(getattr(clazz, method_name))


class ClassVisitor(object):

    _classes = []
    _modules = []

    def __init__(self, sub_module, filter=lambda clazz: True):
        self._sub_module = sub_module
        self._filter = filter

    def _load_classes(self):
        if self._sub_module in ClassVisitor._modules:
            return

        import importlib

        command_module = importlib.import_module(
            "." + self._sub_module, __package__)

        import pkgutil
        import inspect

        classes = []
        for importer, modulename, ispkg in pkgutil.iter_modules(command_module.__path__):
            submodule = importlib.import_module(
                "{}.{}.{}".format(__package__, self._sub_module, modulename))
            for class_name, clazz in inspect.getmembers(submodule, predicate=inspect.isclass):
                for method_name, method in inspect.getmembers(clazz, predicate=inspect.isfunction):
                    classes.append(clazz)
                    break

        ClassVisitor._classes += classes
        ClassVisitor._modules += [self._sub_module]

    def _parent_module_name(self, module):
        module_name = str(module)

        return module_name[:module_name.rfind(".")]

    def _is_at_sub_module(self, clazz):
        clazz_parent_module_name = self._parent_module_name(clazz.__module__)

        self_parent_module_name = self._parent_module_name(self.__module__)

        target_module_name = self_parent_module_name + "." + self._sub_module

        return target_module_name == clazz_parent_module_name

    def visit(self, visitor):
        self._load_classes()

        for clazz in ClassVisitor._classes:
            if self._is_at_sub_module(clazz):
                if self._filter(clazz):
                    visitor(clazz)
