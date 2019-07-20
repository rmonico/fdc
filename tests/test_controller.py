#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
from unittest import TestCase

from di_container.controller import controller
from di_container.injector import di_container


class TestEventHandler(object):

    def no_parameter_event_handler(self):
        global _test_event_handled
        _test_event_handled = True

    def parametrized_event_handler(self, parameter):
        global _test_event_parameter
        _test_event_parameter = 41


class EventHandlerWillReturnData(object):

    def event_that_will_return_data_handler(self):
        return 'status', {'property1': 'key-value data 1 value',
                'property2': 'software é como lingüiça: melhor não saber como é feito'}, 'first data', \
               'second data'


class ControllerTestCase(TestCase):

    def test_event_triggered(self):
        di_container.load_resources(['commons'])
        controller.load_listeners([__package__])

        global _test_event_handled
        _test_event_handled = False

        controller.event('no_parameter_event')

        self.assertTrue(_test_event_handled)

    def test_parametrized_event_trigger(self):
        di_container.load_resources(['commons'])
        controller.load_listeners([__package__])

        global _test_event_parameter
        _test_event_parameter = -1

        controller.event('parametrized_event', parameter=41)

        self.assertEqual(_test_event_parameter, 41)

    def test_event_which_return_data(self):
        di_container.load_resources(['commons'])
        controller.load_listeners([__package__])

        results = controller.event('event_that_will_return_data')

        self.assertIsInstance(results, list)

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.status, 'status')
        self.assertEqual(result.data, ('first data', 'second data'))
        self.assertEqual(result.kwdata['property1'], 'key-value data 1 value')
        self.assertEqual(result.kwdata['property2'], 'software é como lingüiça: melhor não saber como é feito')


if __name__ == '__main__':
    unittest.main()
