#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from unittest import TestCase

from di_container.methodvisitor import MethodVisitor


class VisitedClass(object):

    def visited_method(self):
        pass


class MethodVisitorTestCase(TestCase):

    def _update_visited_method_list(self, clazz, method):
        self._visited += [(clazz.__name__, method.__name__)]

    def _reset_visited_method_list(self):
        self._visited = []

    def test_visit(self):
        visitor = MethodVisitor([__package__], lambda clazz,
                                                      method: clazz.__name__ == 'VisitedClass' and method.__name__ == 'visited_method')

        self._reset_visited_method_list()

        visitor.visit(self._update_visited_method_list)

        self.assertEqual(self._visited, [('VisitedClass', 'visited_method')])


if __name__ == '__main__':
    unittest.main()
