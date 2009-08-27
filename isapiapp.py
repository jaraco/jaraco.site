#!python

from jaraco.site.isapi import (
	factory as __ExtensionFactory__,
	handle_command_line, setup_environment,
	)
setup_environment(__file__)
if __name__ == '__main__': handle_command_line()
