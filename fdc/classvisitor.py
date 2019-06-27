#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ClassVisitor(object):

    _classes = []
    _modules = []

    def __init__(self, sub_module):
        self._sub_module = sub_module

    def _load_classes(self):
        if self._sub_module in self._modules:
            return

        import importlib

        command_module = importlib.import_module("." + self._sub_module, __package__)

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

        return classes

    def visit(self, client):
        for clazz in self._classes:
            if str(clazz.__module__) == self._sub_module:
                client(clazz)
