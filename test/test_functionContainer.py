#!/usr/bin/env python
# vim:set softtabstop=4 shiftwidth=4 tabstop=4 expandtab:
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

from test import prompty
from test import UnitTestWrapper


class MyFunctions(prompty.functionBase.PromptyFunctions):
    def test_func(self):
        return "This Is A Test"

    def _hidden_func(self):
        return "This is secret"


class FunctionContainerTests(UnitTestWrapper):
    def test_noname(self):
        c = prompty.functionContainer.FunctionContainer()
        self.assertRaises(TypeError, c._call)

    def test_extendFunctionContainer(self):
        c = prompty.functionContainer.FunctionContainer()
        # Import this module
        c.add_functions_from_module(sys.modules[__name__])
        self.assertEqual(r"This Is A Test", c._call("test_func"))
        self.assertRaises(KeyError, c._call, "_hidden_func")

    def test_extendFunctionContainerFromDir(self):
        c = prompty.functionContainer.FunctionContainer()
        # Import this directory
        c.add_functions_from_dir(os.path.dirname(sys.modules[__name__].__file__))
        self.assertEqual(r"This Is A Test", c._call("test_func"))
