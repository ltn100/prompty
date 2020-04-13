#!/usr/bin/env python
# vim:set softtabstop=4 shiftwidth=4 tabstop=4 expandtab:
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from builtins import str

from prompty import parser
from prompty import colours
from prompty import status


class Compiler(object):
    """ Compiles and executes the parsed dictionary list output
    from the Parser.

    Literals are output verbatim, or passed into functions for
    processing.
    """
    def __init__(self, function_container):
        # Compiler requires a valid FunctionContainer in order
        # to execute functions
        self.funcs = function_container

        self.parser = parser.Parser()
        self.parsed_struct = []

    def clear(self):
        """
        Clear the compiled struct
        """
        self.parsed_struct = []

    def compile(self, prompt_string, clear=True):
        """ Parse a given prompt_string. Add the resulting
        list of dictionary items to the internal buffer
        ready for executing.
        """
        if clear:
            self.clear()
        self.parsed_struct.extend(self.parser.parse(prompt_string))

    def execute(self):
        """ Execute the internal buffer and return the output
        string.
        """
        return self._execute(self.parsed_struct)

    def _move(self, string):
        self.funcs.status.pos.inc_from_string(string)
        return string

    def _execute(self, parsed_struct):
        out = u""
        for element in parsed_struct:
            if element['type'] == 'literal':
                # Literals go to the output verbatim
                out += self._move(element['value'])
            elif element['type'] == 'function':
                # First arg is the function name and current char position
                args = [element['name']]
                # Then the required arguments
                if 'args' in element:
                    for arg in element['args']:
                        args.append(self._execute(arg))
                # Finally any optional arguments
                if 'optargs' in element:
                    for optarg in element['optargs']:
                        args.append(self._execute(optarg))
                # Call the function!
                try:
                    out += self._move(str(self.funcs._call(*args)))
                except ValueError as e:
                    return "Prompty error on line %d: %s\n$ " % (element['lineno'], str(e))
                except KeyError as e:
                    return "Prompty error on line %d: No such function %s\n$ " % (element['lineno'], str(e))

        return out
