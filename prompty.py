#!/usr/bin/env python
# vim:set softtabstop=4 shiftwidth=4 tabstop=4 expandtab:

# Import external modules
import sys
import getopt


USAGE = "Usage: %s [options]" % sys.argv[0] + """
Options:     -h, --help      Display this help message and exit
"""

def usage(msg=''):
    """Print usage information to stderr.

    @param msg: An optional message that will be displayed before the usage
    @return: None
    """
    if msg:
        print >> sys.stderr, msg
    print >> sys.stderr, USAGE


class Prompt(object):
    def __init__(self):
        pass

    def getPrompt(self):
        return "\u@\h\$ "


def main(argv=None):
    """Main function. This is the entry point for the program and is run when
    the script is executed stand-alone (i.e. not included as a module

    @param argv: A list of argumets that can over-rule the command line arguments.
    @return: Error status
    @rtype: int
    """
    # Use the command line (system) arguments if none were passed to main
    if argv is None:
        argv = sys.argv


    # Parse command line options
    try:
        opts, args = getopt.getopt(argv[1:], "hb", ["help", "bash"])
    except getopt.error, msg:
        usage(msg)
        return 1

    # Defaults

    # Act upon options
    for option, arg in opts:
        if option in ("-h","--help"):
            usage()
            return 0

        if option in ("-b", "--bash"):
            print "export PS1=\"$(%s)\"" % sys.argv[0]
            return 0

    #if len(args) < 0:
    #    usage("Not enough arguments")
    #    return 1


    p = Prompt()
    sys.stdout.write(p.getPrompt())

    return 0




#---------------------------------------------------------------------------#
#                          End of functions                                 #
#---------------------------------------------------------------------------#
# Run main if this file is not imported as a module
if __name__ == "__main__":
    sys.exit(main())
