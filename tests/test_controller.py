#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from unittest import TestCase

from di_container.controller import controller


class TestEventHandler(object):

    def no_parameter_event_handler(self):
        global _test_event_handled
        _test_event_handled = True

    def parametrized_event_handler(self, parameter):
        global _test_event_parameter
        _test_event_parameter = 41


class ControllerTestCase(TestCase):

    def test_event_triggered(self):
        controller.load_listeners([__package__])

        global _test_event_handled
        _test_event_handled = False

        controller.event('no_parameter_event')

        self.assertTrue(_test_event_handled)

    def test_parametrized_event_trigger(self):
        controller.load_listeners([__package__])

        global _test_event_parameter
        _test_event_parameter = -1

        controller.event('parametrized_event', parameter=41)

        self.assertEqual(_test_event_parameter, 41)

if __name__ == '__main__':
    unittest.main()
